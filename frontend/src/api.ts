import { paths } from './openapi-schema'
import { Fetcher, Middleware } from 'openapi-typescript-fetch'


export function storeAuthToken(token: string | undefined) {
  if (token) {
    localStorage.setItem('auth', token);
  } else {
    localStorage.removeItem('auth');
  }
}

const authMiddleware: Middleware = async (url, init, next) => {
  const headers: Headers = new Headers();

  const authToken = localStorage.getItem('auth');
  if (authToken) {
    headers.set('Authorization', `Token ${authToken}`);
  }

  if (typeof init.body == 'string') {
    headers.set('Content-Type', 'application/json');
  }

  const response = await next(url, {...init, headers: headers})
  return response
}

const fetcher = Fetcher.for<paths>()
fetcher.configure({
  baseUrl: '/',
  use: [authMiddleware]
})


export const login = fetcher.path('/api/v1/users/login/').method('post').create()