export function toJson(data) {
  let jsonData = {};
  data.forEach((value, key) => jsonData[key] = value);
  return jsonData
}


export function debounce(fn, delay = 300) {
  let timeout;
  return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => fn(...args), delay);
  };
}