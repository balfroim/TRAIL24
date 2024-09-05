export const apiBaseUrl = import.meta.env.DEV ? "http://localhost:8000" : "";

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
  console.log(import.meta.env.DEV);
  console.log(response);
  if (!response.ok) {
    throw new Error("API error");
  } else if (endpoint === "rate") {
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

export async function deleteRateApiCall(userId, productId) {
  return await genericApiCall("rate", `${userId}/${productId}`, "DELETE", {})
}

export async function getRecommendationsApiCall(userId) {
  return await genericApiCall("rec", userId, "GET", {})
}

export async function getExplanationApiCall(userId, productId) {
  return await genericApiCall("explain", `${userId}/${productId}`, "GET", {});
}

export async function setProfileApiCall(data) {
  return await genericApiCall("set_profile", "", "POST", data);
}

export async function getPosterApiCall(productId) {
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "image/jpeg");

  const url = `${apiBaseUrl}/poster/${productId}`;

  const options = {
    method: "GET",
    headers: myHeaders,
  };

  const response = await fetch(url, options);
  console.log(response);
  return response.ok;
}
