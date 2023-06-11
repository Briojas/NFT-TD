// This example shows how to make a decentralized price feed using multiple APIs

// Arguments can be provided when a request is initated on-chain and used in the request source code as shown below
const main_cid = args[0];
const unique_cids_required = 1; //TODO: make this an argument
const results_header = "000-";

// To make an HTTP request, use the Functions.makeHttpRequest function
// Functions.makeHttpRequest function parameters:
// - url
// - method (optional, defaults to 'GET')
// - headers: headers supplied as an object (optional)
// - params: URL query parameters supplied as an object (optional)
// - data: request body supplied as an object (optional)
// - timeout: maximum request duration in ms (optional, defaults to 10000ms)
// - responseType: expected response type (optional, defaults to 'json')

//grab the tower data requesting to be minted
const main_data = Functions.makeHttpRequest({
  url: "https://ipfs.io/ipfs/" + main_cid + "/tower.json",
});
const [main_data_response] = await Promise.all([main_data]);
sub_cid_names = Object.keys(main_data_response.data.properties);
var sub_cids = [];
var cid_query = "(";
for (var i = 0; i < sub_cid_names.length; i++) {
  var sub_cid = main_data_response.data.properties[sub_cid_names[i]];
  cid_query = cid_query + "'" + sub_cid.id + "',";
  sub_cids.push(sub_cid.id);
}
cid_query = cid_query.slice(0, -1) + ")";
// console.log(cid_query)

//search for existing data with requested sub cids
const resourceId = "PRIME_CRUSADERS.CARDS"; //TODO: make this an argument
const id_name = "CARD"; //TODO: make this an argument
const query_sqlText =
  "SELECT " +
  id_name +
  " FROM " +
  resourceId +
  " WHERE " +
  id_name +
  " IN " +
  cid_query;
const url = `${secrets.sxtUrl}sql/dql`;
const token = `Bearer ${secrets.accessToken}`;
const existing_data = await Functions.makeHttpRequest({
  url: `${secrets.sxtUrl}sql/dql`,
  method: "POST",
  timeout: 4500,
  headers: {
    Authorization: `Bearer ${secrets.accessToken}`,
    "Content-Type": "application/json",
  },
  data: { resourceId: resourceId, sqlText: query_sqlText },
});
const existing_data_response = existing_data.data;
console.log(existing_data_response);
var existing_cids = [];
for (var i = 0; i < existing_data_response.length; i++) {
  existing_cids.push(existing_data_response[i][id_name]);
}
// console.log(sub_cids)
// console.log(existing_cids)

//check how many sub cids of the nft requesting to be minted already existed
const new_cids = sub_cids.filter((x) => !existing_cids.includes(x));
var results = "";
var new_cids_sqlText = "";
if (new_cids.length >= unique_cids_required) {
  results = results_header + "1";
  //build sqlText to insert new cids into the database
  for (var i = 0; i < new_cids.length; i++) {
    for (var j = 0; j < sub_cids.length; j++) {
      const cid_data = main_data_response.data.properties[sub_cid_names[i]];
      if (cid_data.id == new_cids[i]) {
        //TODO: feed data 'name' fields in as argument?
        new_cids_sqlText =
          new_cids_sqlText +
          "('" +
          cid_data.id +
          "'," + //adding single quotes around the id to make it a string
          cid_data.teir +
          "," +
          cid_data.priority +
          "," +
          cid_data.operator +
          "," +
          cid_data.data1 +
          "," +
          cid_data.data2 +
          "," +
          cid_data.data3 +
          "),";
        break;
      }
    }
  }
} else {
  results = results_header + "0";
}

// if a new tower is to be minted, its new cids are added to the database
if (new_cids_sqlText.length > 0) {
  new_cids_sqlText = new_cids_sqlText.slice(0, -1);
  //store new cids in the database
  const modify_sqlText =
    "INSERT INTO " +
    resourceId +
    " (card,teir,priority,operator,data1,data2,data3) VALUES " +
    new_cids_sqlText;
  const cid_data = await Functions.makeHttpRequest({
    url: `${secrets.sxtUrl}sql/dml`,
    method: "POST",
    timeout: 4500,
    headers: {
      Authorization: `Bearer ${secrets.accessToken}`,
      "Content-Type": "application/json",
      biscuit: `${secrets.biscuit}`,
    },
    data: { resourceId: resourceId, sqlText: modify_sqlText },
  });
  console.log(cid_data);
}

// The source code MUST return a Buffer or the request will return an error message
// Use one of the following functions to convert to a Buffer representing the response bytes that are returned to the client smart contract:
// - Functions.encodeUint256
// - Functions.encodeInt256
// - Functions.encodeString
// Or return a custom Buffer for a custom byte encoding
// return Functions.encodeUint256(Math.round(prices[0] * 100));
const buffer = Buffer.from(results, "utf8");
return buffer;
