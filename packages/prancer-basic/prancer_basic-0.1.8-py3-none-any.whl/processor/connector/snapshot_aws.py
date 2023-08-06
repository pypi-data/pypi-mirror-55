"""
snapshot connector file for aws type snapshot. When the 'type' is 'aws', the
resource objects have to be fetched from the AWS interface.
The connection could use python SDK libraries or https calls or other known methods
provided by the provider.
Here in case of AWS, have used boto python SDK released and maintained by AWS.
boto library provides different 'describe_' functions and using this functionality,
the snapshot mentions which describe function has to be called, so 'type' could
be 'security_groups' , 'instances', 'regions' and using python reflection capabilities
a callable from describe_security_groups gets callable for this function to return security groups.
The describe_ functions lots of methods to query AWS resources, since we know what resource we need
we always query by id, so AWS snapshots shall always have {"id": "123de23"} to uniquely
identify the resource object.
"""
import json
import hashlib
import time
from boto3 import client
from boto3 import Session
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import put_in_currentdata, get_dbtests
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    collectiontypes, STRUCTURE, make_snapshots_dir, store_snapshot
from processor.connector.vault import get_vault_data
from processor.helper.config.config_utils import config_value, get_test_json_dir
from processor.database.database import insert_one_document, sort_field, get_documents,\
    COLLECTION, DATABASE, DBNAME
from processor.helper.httpapi.restapi_azure import json_source
from processor.helper.httpapi.restapi_azure import get_client_secret
from processor.connector.snapshot_utils import validate_snapshot_nodes


logger = getlogger()
_valid_service_names = Session().get_available_services()


def _validate_client_name(client_name):
    """
    A private function to validate whether a given client provided
    in snapshot or aws connector is a valid service in Boto3
    """
    return client_name.lower() in _valid_service_names


def get_aws_data(snapshot_source):
    """
    The AWS source object to be fetched from database or the filesystem
    The initial configuration for database is 'validator' and collection
    is 'structures', whereas for the filesystem the path to fetch the
    'structures' is  $SOLUTIONDIR/realm/<structure>.json
    """
    sub_data = {}
    if json_source():
        dbname = config_value(DATABASE, DBNAME)
        collection = config_value(DATABASE, collectiontypes[STRUCTURE])
        parts = snapshot_source.split('.')
        qry = {'name': parts[0]}
        sort = [sort_field('timestamp', False)]
        docs = get_documents(collection, dbname=dbname, sort=sort, query=qry, limit=1)
        logger.info('Number of AWS structure Documents: %d', len(docs))
        if docs and len(docs):
            sub_data = docs[0]['json']
    else:
        json_test_dir = get_test_json_dir()
        file_name = '%s.json' % snapshot_source if snapshot_source and not \
            snapshot_source.endswith('.json') else snapshot_source
        aws_source = '%s/../%s' % (json_test_dir, file_name)
        logger.info('AWS source: %s', aws_source)
        if exists_file(aws_source):
            sub_data = json_from_file(aws_source)
    return sub_data


def _get_aws_function(awsclient, node):
    """ 
    A private function to get the function which has to be called by the
    boto3 client object to get snapshot data.
    """
    describe_function_str = get_aws_describe_function(node)
    if describe_function_str:
        describe_function = getattr(awsclient, describe_function_str, None)
        if describe_function and callable(describe_function):
            return describe_function
    
    function_str = _get_callable_method_from_node(node)
    if function_str:
        callable_function = getattr(awsclient, function_str, None)
        if callable_function and callable(callable_function):
            return callable_function

    
def _get_callable_method_from_node(node):
    """Callable Method from node using python reflection mechanism"""
    _fn_str = None
    if node and 'type' in node and node['type']:
        _fn_str = node['type']
    return _fn_str
    

def get_aws_describe_function(node):
    """Describe function for the node using python reflection mechanism"""
    describe_fn_str = None
    if node and 'type' in node and node['type']:
        describe_fn_str = 'describe_%s' % node['type']
    return describe_fn_str


def get_node(awsclient, node, snapshot_source):
    """
    Fetch node from aws using connection. In this case using boto API's
    describe functions.
    """

    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    function_to_call = None
    db_record = {
        "structure": "aws",
        "error": None,
        "reference": "",
        "source": parts[0],
        "path": '',
        "timestamp": int(time.time() * 1000),
        "queryuser": "",
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'],
        "collection": collection.replace('.', '').lower(),
        "json": {}  # Refactor when node is absent it should None, when empty object put it as {}
    }
    function_to_call = _get_aws_function(awsclient, node)
    if function_to_call and callable(function_to_call):
        queryval = get_field_value(node, 'id')
        try:
            data = function_to_call(**queryval)
            if data:
                db_record['json'] = data
                checksum = get_checksum(data)
                if checksum:
                    db_record['checksum'] = checksum
                else:
                    put_in_currentdata('errors', data)
                    logger.info("Describe function does not exist: %s", str(function_to_call))
                    db_record['error'] = "Describe function does not exist: %s" % str(function_to_call)
        except Exception as ex:
            logger.info('Describe function exception: %s', ex)
            db_record['error'] = 'Describe function exception: %s' % ex
    else:
        logger.info('Invalid function exception: %s', str(function_to_call))
        db_record['error'] = 'Invalid function exception: %s' % str(function_to_call)
    return db_record


def get_checksum(data):
    """ Get the checksum for the AWS data fetched."""
    checksum = None
    try:
        data_str = json.dumps(data)
        checksum = hashlib.md5(data_str.encode('utf-8')).hexdigest()
    except:
        pass
    return checksum

def populate_aws_snapshot(snapshot, container):
    """
    This is an entrypoint for populating a snapshot of type aws.
    All snapshot connectors should take snapshot object and based on
    'source' field create a method to connect to the service for the
    connector.
    The 'source' field could be used by more than one snapshot, so the
    'testuser' attribute should match to the user the 'source'
    """
    dbname = config_value('MONGODB', 'dbname')
    snapshot_source = get_field_value(snapshot, 'source')
    snapshot_user = get_field_value(snapshot, 'testUser')
    sub_data = get_aws_data(snapshot_source)
    snapshot_nodes = get_field_value(snapshot, 'nodes')
    snapshot_data, valid_snapshotids = validate_snapshot_nodes(snapshot_nodes)
    # valid_snapshotids = True
    # if snapshot_nodes:
    #     for node in snapshot_nodes:
    #         snapshot_data[node['snapshotId']] = False
    #         if not isinstance(node['snapshotId'], str):
    #             valid_snapshotids = False
    # if not valid_snapshotids:
    #     logger.error('All snap')
    if valid_snapshotids and sub_data and snapshot_nodes:
        logger.debug(sub_data)
        access_key, secret_access, region, connector_client_str = \
            get_aws_client_data(sub_data, snapshot_user)
        if not access_key:
            logger.info("No access_key in the snapshot to access aws resource!...")
            return snapshot_data
        if not secret_access:
            secret_access = get_vault_data(access_key)
            logger.info('Vault Secret: %s', '*' * len(secret_access))
        if not secret_access:
            secret_access = get_client_secret()
            logger.info('Environment variable or Standard input, Secret: %s', '*' * len(secret_access))
        if not secret_access:
            logger.info("No secret_access in the snapshot to access aws resource!...")
            return snapshot_data
        if access_key and secret_access:
            existing_aws_client = {}
            # This will track exisitng AWS client objects to prevent creating redudant clients. 
            for node in snapshot['nodes']:
                client_str = get_field_value(node, 'client')
                if not client_str:
                    logger.info("No client type provided in snapshot, using client type from connector")
                    client_str = connector_client_str
                else:
                    if not _validate_client_name(client_str):
                        logger.error("Invalid Client Name")
                        return snapshot_data
                aws_region = get_field_value(node, 'region')
                if not aws_region:
                    logger.info("No region provided in snapshot, using region from connector")
                    aws_region = region
                try:
                    awsclient = existing_aws_client.get(client_str.lower(), None)

                    if not awsclient:
                        awsclient = client(client_str.lower(), aws_access_key_id=access_key,
                                           aws_secret_access_key=secret_access, region_name=aws_region)
                except Exception as ex:
                    logger.info('Unable to create AWS client: %s', ex)
                    awsclient = None
                logger.info(awsclient)
                if awsclient:
                    existing_aws_client[client_str.lower()] = awsclient
                    data = get_node(awsclient, node, snapshot_source)
                    if data:
                        error_str = data.pop('error', None)
                        if get_dbtests():
                            insert_one_document(data, data['collection'], dbname)
                        else:
                            snapshot_dir = make_snapshots_dir(container)
                            if snapshot_dir:
                                store_snapshot(snapshot_dir, data)
                        snapshot_data[node['snapshotId']] = False if error_str else True
    return snapshot_data


def get_aws_client_data(aws_data, snapshot_user):
    """
    AWS client information as required by the Boto client, viz access_key
    access_secret, AWS command type like EC2, S3 etc and region
    The access_secret is either read from structure json or env variable or keyvault
    """
    accesskey = None
    secret_access = None
    region = None
    client_str = None
    if aws_data and snapshot_user:
        org_units = get_field_value(aws_data, "organization-unit")
        if org_units:
            found = False
            for org_unit in org_units:
                accounts = get_field_value(org_unit, 'accounts')
                if accounts:
                    for account in accounts:
                        users = get_field_value(account, 'users')
                        if users:
                            for user in users:
                                username = get_field_value(user, 'name')
                                if username and username == snapshot_user:
                                    found = True
                                    accesskey = get_field_value(user, 'access-key')
                                    secret_access = get_field_value(user, 'secret-access')
                                    region = get_field_value(user, 'region')
                                    client_str = get_field_value(user, 'client')
                                    if client_str and not _validate_client_name(client_str):
                                        logger.error("Invalid Client Name")
                                    break
                        if found:
                            break
                if found:
                    break
    return accesskey, secret_access, region, client_str
