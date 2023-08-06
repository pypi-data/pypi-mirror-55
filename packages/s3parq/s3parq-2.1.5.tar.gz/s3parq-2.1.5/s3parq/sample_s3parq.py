
from dfmock import dfmock
import publish_parq as parq


columns = { "hamburger":{"option_count":3, "option_type": "string"},
            "hot_dog":{"option_count":5, "option_type": "integer"},
            "shoelace":"string"
          }

dfmocker = dfmock.DFMock(count=100, columns=columns, )
dfmocker.generate_dataframe()
my_mocked_dataframe = dfmocker.dataframe
bucket = 'ichain-dev'
key = 'retrodemo1/data'
parq.publish(bucket=bucket, key=key, dataframe=my_mocked_dataframe, partitions=['hamburger','hot_dog'])

