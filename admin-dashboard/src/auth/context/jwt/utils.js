import Cookies from 'js-cookie';

import axios from 'src/utils/axios';

export function setCookie(name, value, days) {
  if (days) {
    const expires = days;
    Cookies.set(name, value, { expires });
  } else {
    Cookies.set(name, value);
  }
}

export function getCookie(name) {
  return Cookies.get(name);
}

function eraseCookie(name) {
  Cookies.remove(name);
}

export const setSession = (accessToken) => {
  if (accessToken) {
    axios.defaults.headers.common.Authorization = `Bearer ${accessToken}`;
  } else {
    eraseCookie('accessToken');
    delete axios.defaults.headers.common.Authorization;
  }
};
