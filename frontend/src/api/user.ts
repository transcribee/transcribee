import { fetcher, makeSwrHook } from '../api';

export const login = fetcher.path('/api/v1/users/login/').method('post').create();
export const getMe = fetcher.path('/api/v1/users/me/').method('get').create();

export const useGetMe = makeSwrHook('getMe', getMe);
