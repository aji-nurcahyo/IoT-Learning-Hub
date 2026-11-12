export function normalizeBase(value = '/iot-learning-hub/') {
  if (!/^\/(?:[a-zA-Z0-9_-]+\/)*[a-zA-Z0-9_-]*\/?$/.test(value)) throw new Error('Base harus berupa path absolut: /, /iot-learning-hub/, atau /kelas/iot/.');
  return value.endsWith('/') ? value : `${value}/`;
}
