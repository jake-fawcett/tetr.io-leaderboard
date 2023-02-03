import pandas as pd
from azure.data.tables import TableClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient

SUBSCRIPTION_ID = "2293b5f9-5144-48c3-9e63-605f45ecbc1e"
GROUP_NAME = "platform-tetris-dev"
STORAGE_ACCOUNT_NAME = "stractdev"


def get_storage_account_key():
    credential = DefaultAzureCredential()

    storage_client = StorageManagementClient(credential, SUBSCRIPTION_ID)
    storage_keys = storage_client.storage_accounts.list_keys(GROUP_NAME, STORAGE_ACCOUNT_NAME)
    storage_keys = {v.key_name: v.value for v in storage_keys.keys}

    key = storage_keys["key2"]
    return key


def get_leaderboard_data():
    account_key = get_storage_account_key()
    table_client = TableClient.from_connection_string(
        conn_str=f"DefaultEndpointsProtocol=https;AccountName={STORAGE_ACCOUNT_NAME};AccountKey={account_key};EndpointSuffix=core.windows.net", table_name="users"
    )
    my_filter = "PartitionKey eq 'Users'"
    entities = table_client.query_entities(query_filter=my_filter, select=["User", "MMR"])

    pd.set_option("display.width", 1000)
    pd.set_option("colheader_justify", "center")

    leaderboard_df = pd.DataFrame(entities)
    sort = leaderboard_df.sort_values(by=["MMR"], ascending=False)
    tables = sort.to_html(classes="leaderboard", header="true", index=False)
    return tables


def calc_mmr(winner_mmr, loser_mmr):
    total_mmr = winner_mmr + loser_mmr
    mmr_change = (loser_mmr / total_mmr) * 200
    winner_mmr += mmr_change
    loser_mmr -= mmr_change
    return winner_mmr, loser_mmr
