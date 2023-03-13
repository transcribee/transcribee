import { fetcher, makeSwrHook } from '../api';

export const listDocuments = fetcher.path('/api/v1/documents/').method('get').create();
export const createDocument = fetcher.path('/api/v1/documents/').method('post').create();

export const createDocumentFormData = async (name: string, audio_file: Blob) => {
  // TODO: fix
  const formData = new FormData();
  formData.append('name', name);
  formData.append('audio_file', audio_file);

  return createDocument({} as any, {
    body: formData,
  });
};

export const getDocument = fetcher.path('/api/v1/documents/{id}/').method('get').create();

export const useListDocuments = makeSwrHook('listDocuments', listDocuments);
export const useGetDocument = makeSwrHook('getDocument', getDocument);
