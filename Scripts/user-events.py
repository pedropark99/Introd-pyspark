
import pandas

data = pandas.DataFrame({
  "dateOfEvent": "15/06/2022",
  "timeOfEvent": ["15/06/2022 14:33:10", "15/06/2022 14:40:08", "15/06/2022 15:48:41"],
  "userId": "b902e51e-d043-4a66-afc4-a820173e1bb4",
  "nameOfEvent": ["entry", "click: shop", "select: payment-method"]
})


data.to_json("Data/user-events.json")