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
import { Class } from '../models/class.model';
import { ClassService } from '../services/class.service';

import { tapResponse } from '@ngrx/operators';
import { Student } from '../../students/models/student.model';
import { User } from '../../users/models/user.model';
interface ClassState {
    class: Class | undefined;
    classes: Class[];
    total: number;
    isLoading: boolean;
    error: string | null;
    query: {
        limit: number;
        offset: number;
        search: string | undefined;
        isActive: boolean | undefined;
    };
}

const initialState: ClassState = {
    class: undefined,
    classes: [],
    total: 0,
    isLoading: false,
    error: null,
    query: {
        limit: 10000,
        offset: 0,
        search: undefined,
        isActive: true
    }
};

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

export const ClassStore = signalStore(
    { providedIn: 'root', protectedState: false },
    withState(initialState),
    //withLogger('classes'),
    withMethods((store, errorHandler = inject(ErrorHandler), service = inject(ClassService)) => ({
        updateQuery(query: { limit: number; offset: number; search?: string; isActive?: boolean }) {
            patchState(store, { query: { ...store.query(), ...query } });
        },

        setClass(classItem: Class) {
            patchState(store, { class: classItem });
        },
        loadClass(id: string) {
            patchState(store, { isLoading: true });
            service.getClass(id).pipe(
                tapResponse({
                    next: (_class) => {
                        patchState(store, { class: _class });
                    },
                    error: (error) => {
                        console.error(error);
                    },
                    finalize: () => {
                        patchState(store, { isLoading: false });
                    },
                })
            ).subscribe();
        },

        removeStudentFromClass(student: Student) {
            if (store.class()) {
                store.class()!.students = store.class()!.students.filter(s => s._id !== student._id);
                this.update(store.class()!);
            }
        },

        removeTeacherFromClass(teacher: User) {
            if (store.class()) {
                store.class()!.teachers = store.class()!.teachers.filter(t => t._id !== teacher._id);
                this.update(store.class()!);
            }
        },


        addStudentToClass(student: Student) {
            if (store.class()) {
                if (!store.class()?.students.some(s => s._id === student._id)) {
                    store.class()?.students.push(student);
                    this.update(store.class()!);
                }
            }
        },
        addTeacherToClass(teacher: User) {
            if (store.class()) {
                if (!store.class()?.teachers.some(t => t._id === teacher._id)) {
                    store.class()?.teachers.push(teacher);
                    this.update(store.class()!);
                }
            }
        },
        update(classItem: Class) {
            patchState(store, { isLoading: true });
            service
                .updateClass(classItem._id!, classItem)
                .pipe(
                    tapResponse({
                        next: (updatedClass) => {
                            patchState(store, {
                                classes: store.classes().map((c) =>
                                    c._id === updatedClass._id && c.is_active === this.query().isActive ? updatedClass : c
                                ),
                            });

                            if (store.class() && store.class()?._id === updatedClass._id) {
                                patchState(store, { class: updatedClass });
                            }
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

        create(classItem: Class) {
            patchState(store, { isLoading: true });
            service
                .createClass(classItem)
                .pipe(
                    tapResponse({
                        next: (newClass) => {
                            patchState(store, {
                                classes: [...store.classes(), newClass],
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

        loadByQuery: rxMethod<{ limit: number; offset: number; search?: string; isActive?: boolean }>(
            pipe(
                debounceTime(300),
                distinctUntilChanged(),
                tap(() => setLoadingStatus(store, true)),
                switchMap((query) => {
                    return service.listClasses(query.limit, query.offset, query.isActive, query.search).pipe(
                        tapResponse({
                            next: (response) => {
                                patchState(store, {
                                    classes: response.classes,
                                    total: response.total
                                });
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