export async function iapi(endpoint, data){
  console.log("Here", `/api/v1/${endpoint}`)
  return fetch(`/api/v1/${endpoint}`, data)
}


export async function papi(fetch, endpoint, data) {
  console.log(`http://server:8000/api/v1/${endpoint}`)
  return fetch(`http://server:8000/api/v1/${endpoint}`, data)
  // return fetch(`https://api.calyps.io/api/v1/${endpoint}`, data)
}