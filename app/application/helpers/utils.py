from azure.data.tables import TableClient
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient


def get_storage_account_key():
    credential = DefaultAzureCredential()
    subscription_id = "TODO:"
    storage_client = StorageManagementClient(credential, subscription_id)
    GROUP_NAME = "TODO:"
    STORAGE_ACCOUNT_NAME = "TODO:"
    storage_keys = storage_client.storage_accounts.list_keys(GROUP_NAME, STORAGE_ACCOUNT_NAME)
    storage_keys = {v.key_name: v.value for v in storage_keys.keys}

    key = (storage_keys['key2'])
    return key


def get_leaderboard_data():
    account_name = "TODO:"
    account_key = get_storage_account_key()
    table_client = TableClient.from_connection_string(
        conn_str=f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net",
        table_name="users")
    my_filter = "PartitionKey eq 'Users'"
    entities = table_client.query_entities(query_filter=my_filter, select=["User", "MMR"])

    pd.set_option('display.width', 1000)
    pd.set_option('colheader_justify', 'center')

    df = pd.DataFrame(entities)
    sort = df.sort_values(by=['MMR'], ascending=False)
    tables = sort.to_html(classes='leaderboard', header="true", index=False)
    return tables


# TODO: Update
def calc_mmr(winner_mmr, loser_mmr):
    total_mmr = winner_mmr + loser_mmr
    mmr_change = (loser_mmr / total_mmr) * 200
    winner_mmr += mmr_change
    loser_mmr -= mmr_change
    return winner_mmr, loser_mmr
