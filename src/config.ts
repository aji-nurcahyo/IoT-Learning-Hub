export const site = {
  name: 'Internet of Things Learning Hub', shortName: 'IoT Learning Hub',
  tagline: 'From Connected Devices to Intelligent Systems',
  creator: 'Aji Pamungkas Tri Nurcahyo', institution: 'Institut Teknologi Sumatera',
  preferenceNamespace: 'iot-learning-hub', repository: 'iot-learning-hub',
};
export const routes = { home: '/', chapters: '/chapters', started: '/getting-started', tracks: '/tracks', about: '/about', template: '/templates', chapter: (id:number) => `/chapter/${id}`, level: (id:number) => `/level/${id}`, track: (id:string) => `/track/${id}` };
export const href = (route:string) => `#${route}`;
export const assetUrl = (path:string) => `${import.meta.env.BASE_URL}${path.replace(/^\/+/, '')}`;
