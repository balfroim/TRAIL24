
const apiBaseUrl = "http://127.0.0.1:8000";

async function genericApiCall(endpoint, query_params, method, data) {
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  let url = `${apiBaseUrl}/${endpoint}`;
  if (query_params) {
    url = `${url}/${query_params}`;
  }

  const options = {
    method: method,
    headers: myHeaders,
  };
  if (method === "POST") {
    options.body = JSON.stringify(data);
  }

  const response = await fetch(url, options);
  console.log(response);
  if (endpoint === "rate") {
    return true
  } else {
    return await response.json()
  }
}

export async function searchApiCall(data) {
  return await genericApiCall("search", '', "POST", data);
}

export async function addRateApiCall(data, userId) {
  return await genericApiCall("rate", userId, "POST", data);
}

export async function getRecommendationApiCall(userId) {
  return await genericApiCall("rec", userId, "GET", {})
}

export async function getExplanationApiCall(userId) {
  return await genericApiCall("explain", userId, "GET", {});
}

export async function setProfile(data) {
  return await genericApiCall("set_profile", "", "POST", data)
}
