// This example shows how to make a decentralized price feed using multiple APIs

// Arguments can be provided when a request is initated on-chain and used in the request source code as shown below
const ipfs_url = args[0];
const results = "000-1";
const buffer = Buffer.from(results, "utf-8");

// To make an HTTP request, use the Functions.makeHttpRequest function
// Functions.makeHttpRequest function parameters:
// - url
// - method (optional, defaults to 'GET')
// - headers: headers supplied as an object (optional)
// - params: URL query parameters supplied as an object (optional)
// - data: request body supplied as an object (optional)
// - timeout: maximum request duration in ms (optional, defaults to 10000ms)
// - responseType: expected response type (optional, defaults to 'json')

// Use multiple APIs & aggregate the results to enhance decentralization
// const coinGeckoRequest = Functions.makeHttpRequest({
//   url: `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd`,
// });

// // First, execute all the API requests are executed concurrently, then wait for the responses
// const [coinGeckoResponse] = await Promise.all([coinGeckoRequest]);

// const prices = [];

// if (!coinGeckoResponse.error) {
//   prices.push(coinGeckoResponse.data["bitcoin"].usd);
// } else {
//   console.log("CoinGecko Error");
// }

// The source code MUST return a Buffer or the request will return an error message
// Use one of the following functions to convert to a Buffer representing the response bytes that are returned to the client smart contract:
// - Functions.encodeUint256
// - Functions.encodeInt256
// - Functions.encodeString
// Or return a custom Buffer for a custom byte encoding
// return Functions.encodeUint256(Math.round(prices[0] * 100));
return buffer;
