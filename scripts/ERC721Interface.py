import io
import json
import requests
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


class ERC721AssetInfoClient:

    def __init__(self, itemId):
        self.itemId = itemId


    def FoundationAppFetchingSchema(self):
        # Select your transport with a defined url endpoint
        urlInfo = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/souravinsights/foundation-indexer")

        # Create a GraphQL client using the defined transport
        client = Client(transport=urlInfo, fetch_schema_from_transport=True)

        # Provide a GraphQL query
        queryString = gql(
        """
        {
            tokens(where: {tokenID: \"""" + str(self.itemId) + """\" }) {
                id
                tokenID
                contentURI
                tokenIPFSPath
        }
        }
        """
        )

        # Execute the query on the transport
        response = client.execute(queryString)
        metadataQuery = response['tokens'][0]['contentURI']
        response['tokens'][0]['metadata'] = requests.get(url=metadataQuery).json()
        # print(json.dumps(response, indent=4))

        return response


    def OpenSeaFetchingSchema(self, asset_contract_address_of_nft):
        # Create a Request client using the defined transport
        url = "https://api.opensea.io/api/v1/assets"

        # Provide a GET Request query
        queryString = {"token_ids":self.itemId, "asset_contract_address":asset_contract_address_of_nft, "limit":"1"}

        # Execute the query on the transport
        response = requests.request("GET", url, params=queryString).json()

        return response


    def RaribleFetchingSchema(self):
        # Create a Request client using the defined transport
        urlMeta = "http://api.rarible.com/protocol/v0.1/ethereum/nft/items/" + self.itemId + "/meta"
        urlInfo = "http://api.rarible.com/protocol/v0.1/ethereum/nft/items/" + self.itemId

        # Provide a GET Request query
        queryString = {"itemId": self.itemId}
        
        # Execute the query on the transport
        response = requests.request("GET", urlMeta, params=queryString).json()
        creatorResponse =  requests.request("GET", urlInfo, params=queryString).json()
        if "ipfs://" in response['image']['url']['ORIGINAL']:
            response['image']['url']['ORIGINAL'].replace("ipfs://", "https://ipfs.io/")

        print(json.dumps(response, indent=4, sort_keys=True))


# NFTClient = ERC721AssetInfoClient(1000)
# NFTClient.FoundationAppFetchingSchema()

# NFTClient = ERC721AssetInfoClient(40930059826298205183487168041223830856677554863973398691462482759410010554369)
# NFTClient.OpenSeaFetchingSchema("0x495f947276749ce646f68ac8c248420045cb7b5e")

# NFTClient = ERC721AssetInfoClient("0xd07dc4262bcdbf85190c01c996b4c06a461d2430:0x000000000000000000000000000000000000000000000000000000000006fcc8")
# NFTClient.RaribleFetchingSchema()