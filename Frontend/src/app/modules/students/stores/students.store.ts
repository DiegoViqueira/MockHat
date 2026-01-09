import {
  signalStore,
  withState,
  withMethods,
  patchState,
  withHooks,
  getState,
  signalStoreFeature,
} from '@ngrx/signals';
import { rxMethod } from '@ngrx/signals/rxjs-interop';
import { debounceTime, distinctUntilChanged, pipe } from 'rxjs';
import { switchMap, tap } from 'rxjs/operators';
import { effect, ErrorHandler, inject } from '@angular/core';
import { StudentsService } from '../services/students.service';
import { tapResponse } from '@ngrx/operators';
import { StudentsInitialState, StudentStoreQueryParams } from './students.store.state';
import { Student } from '../models/student.model';

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

export const StudentsStore = signalStore(
  { providedIn: 'root', protectedState: false },
  withState(StudentsInitialState),
  //withLogger('students'),
  withMethods((store, errorHandler = inject(ErrorHandler), service = inject(StudentsService)) => ({
    updateQuery(query: StudentStoreQueryParams) {
      patchState(store, { query });
    },
    update(student: Student) {
      patchState(store, { isLoading: true });
      service
        .update(student)
        .pipe(
          tapResponse({
            next: (newStudent) => {
              patchState(store, {
                students: store.students().map((s) => (s._id === newStudent._id ? newStudent : s)),
              });
            },
            error: (error) => {
              errorHandler.handleError(error);
            },
            finalize: () => {
              patchState(store, { isLoading: false });
            },
          })
        )
        .subscribe();
    },
    create(student: Student) {
      patchState(store, { isLoading: true });
      service
        .create(student)
        .pipe(
          tapResponse({
            next: (newStudent) => {
              patchState(store, {
                students: [...store.students(), newStudent],
              });
            },
            error: (error) => {
              errorHandler.handleError(error);
            },
            finalize: () => {
              patchState(store, { isLoading: false });
            },
          })
        )
        .subscribe();
    },
    loadByQuery: rxMethod<StudentStoreQueryParams>(
      pipe(
        debounceTime(300),
        distinctUntilChanged(),
        tap(() => setLoadingStatus(store, true)),
        switchMap(() => {
          const state = getState(store);
          return service.search(state.query.limit, state.query.offset).pipe(
            tapResponse({
              next: (listStudents) => {
                patchState(store, { students: listStudents.students, total: listStudents.total });
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
    onInit({ loadByQuery, query }) {
      loadByQuery(query);
    },
  })
);
