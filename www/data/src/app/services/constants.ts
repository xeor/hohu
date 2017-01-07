export const MOBILE = (typeof window !== 'undefined') ? (window.screen.availWidth < 800) : true;

export const BASE_HOST: string = `${HOST}:${PORT}`;
export const BASE_URL: string = `${location.protocol}://${BASE_HOST}`;
