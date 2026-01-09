import {
  getState,
  patchState,
  signalStore,
  signalStoreFeature,
  withHooks,
  withMethods,
  withState,
} from '@ngrx/signals';

import { effect, ErrorHandler, inject } from '@angular/core';
import { tapResponse } from '@ngrx/operators';
import { UserStoreInitialState, UserStoreQueryParams } from './user.store.state';
import { UserManagementService } from '../services/user-management.service';
import { rxMethod } from '@ngrx/signals/rxjs-interop';
import { switchMap, tap } from 'rxjs/operators';
import { distinctUntilChanged, debounceTime, pipe } from 'rxjs';

export function withLogger(name: string) {
  return signalStoreFeature(
    withHooks({
      onInit(store) {
        effect(() => {
          const state = getState(store);
          console.log(`${name} state changed`, state);
        });
      },
    })
  );
}

const setLoadingStatus = (store, isLoading) => patchState(store, { isLoading });

export const UserStore = signalStore(
  { providedIn: 'root', protectedState: false },
  withState(UserStoreInitialState),
  //withLogger('user'),
  withMethods((store, service = inject(UserManagementService), errorHandler = inject(ErrorHandler)) => ({
    active() {
      patchState(store, { isLoading: true });
      service
        .me()
        .pipe(
          tapResponse({
            next: (user) => {
              patchState(store, { user: user });
            },
            error: (error) => {
              console.info(error);
            },
            finalize: () => {
              patchState(store, { isLoading: false });
            },
          })
        )
        .subscribe();
    },
    loadByQuery: rxMethod<UserStoreQueryParams>(
      pipe(
        debounceTime(300),
        distinctUntilChanged(),
        tap(() => setLoadingStatus(store, true)),
        switchMap(() => {
          const state = getState(store);
          return service.search(state.query.limit, state.query.offset).pipe(
            tapResponse({
              next: (listUsers) => {
                patchState(store, { users: listUsers.users, total: listUsers.total });
              },
              error: (error) => {
                errorHandler.handleError(error);
              },
              finalize: () => {
                setLoadingStatus(store, false);
              },
            })
          );
        })
      )
    ),
  })),
  withHooks({
    onInit({ active, loadByQuery }) {
      active();
      loadByQuery({ query: '', limit: 1000, offset: 0 });
    },

  })
);
