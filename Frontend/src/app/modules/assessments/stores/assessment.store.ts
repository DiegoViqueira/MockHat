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
import { debounceTime, distinctUntilChanged, pipe, of } from 'rxjs';
import { switchMap, tap } from 'rxjs/operators';
import { effect, ErrorHandler, inject } from '@angular/core';

import { tapResponse } from '@ngrx/operators';
import { Assessment } from '../models/assessment.model';
import { AssessmentService } from '../services/assessment.service';
import { Institution } from '../../shared/models/institutions.enum';
import { ExamType } from '../../shared/models/exam_type.enum';
import { Level } from '../../users/models/user-level.enum';
import { WritingTask } from '../models/writing.task.model';
import { Writing, WritingAIFeedback } from '../models/writing.model';
import { Grammar } from '../models/grammar.model';

interface AssessmentState {
    assessment: Assessment | undefined;
    assessments: Assessment[];
    writings: Writing[];
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

const initialState: AssessmentState = {
    assessment: undefined,
    assessments: [],
    writings: [],
    total: 0,
    isLoading: false,
    error: null,
    query: {
        limit: 10000,
        offset: 0,
        search: undefined,
        isActive: undefined
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

export const AssessmentStore = signalStore(
    { providedIn: 'root', protectedState: false },
    withState(initialState),
    //withLogger('assessments'),
    withMethods((store, errorHandler = inject(ErrorHandler), service = inject(AssessmentService)) => ({
        updateQuery(query: { limit: number; offset: number; search?: string; isActive?: boolean }) {
            patchState(store, { query: { ...store.query(), ...query } });
        },


        updateWritingAIFeedback(assessmentId: string, writingId: string, aiFeedback: WritingAIFeedback) {
            patchState(store, { isLoading: true });
            service.updateWritingAIFeedback(assessmentId, writingId, aiFeedback).pipe(
                tapResponse({
                    next: (updatedAIFeedback) => {
                        patchState(store, { writings: store.writings().map((w) => w.id === writingId ? { ...w, ai_feedback: updatedAIFeedback } : w) });
                    },
                    error: (error) => {
                        errorHandler.handleError(error);
                    },
                })
            ).subscribe();
        },

        updateAssessmentGrammarFeedback(assessmentId: string, writingId: string, grammarFeedback: Grammar) {
            patchState(store, { isLoading: true });
            service.updateAssessmentGrammarFeedback(assessmentId, writingId, grammarFeedback).pipe(
                tapResponse({
                    next: (updatedGrammarFeedback) => {
                        patchState(store, { writings: store.writings().map((w) => w.id === writingId ? { ...w, grammar_feedback: updatedGrammarFeedback } : w) });
                    },
                    error: (error) => {
                        errorHandler.handleError(error);
                    },
                    finalize: () => {
                        patchState(store, { isLoading: false });
                    },
                })
            ).subscribe();
        },

        getAssessmentWritings(assessmentId: string) {
            patchState(store, { isLoading: true });
            service.getAssessmentWritings(assessmentId).pipe(
                tapResponse({
                    next: (writings) => {
                        patchState(store, { writings });
                    },
                    error: (error) => {
                        errorHandler.handleError(error);
                    },
                    finalize: () => {
                        patchState(store, { isLoading: false });
                    },
                })
            ).subscribe();
        },

        updateAssessmentText(assessmentId: string, text: string) {
            patchState(store, { isLoading: true });
            service.updateAssessmentText(assessmentId, text).pipe(
                tapResponse({
                    next: (updatedAssessment) => {
                        patchState(store, {
                            assessments: store.assessments().map((a) => a._id === assessmentId ? updatedAssessment : a),
                            assessment: updatedAssessment
                        });
                    },
                    error: (error) => {
                        errorHandler.handleError(error);
                    },
                    finalize: () => {
                        patchState(store, { isLoading: false });
                    },
                })
            ).subscribe();

        },

        uploadAssessmentWriting(assessmentId: string, studentId: string, files: Blob[]) {
            patchState(store, { isLoading: true });
            service.uploadAssessmentWriting(assessmentId, studentId, files).pipe(
                tapResponse({
                    next: () => {
                    },
                    error: (error) => {
                        errorHandler.handleError(error);
                    },
                    finalize: () => {
                        patchState(store, { isLoading: false });
                    },
                })
            ).subscribe();
        },
        setAssessment(assessment: Assessment) {
            patchState(store, { assessment });
        },

        updateAssessmentState(assessment: Assessment) {
            patchState(store, { assessments: store.assessments().map((a) => a._id === assessment._id ? assessment : a), assessment });
        },

        create(title: string, class_id?: string, institution?: Institution, exam_type?: ExamType, level?: Level, task?: WritingTask, imageBlob?: Blob) {
            patchState(store, { isLoading: true });
            service
                .createAssessment(title, class_id, institution, exam_type, level, task, imageBlob)
                .pipe(
                    tapResponse({
                        next: (newAssessment) => {
                            patchState(store, {
                                assessments: [...store.assessments(), newAssessment],
                                assessment: newAssessment
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

        loadByClassId(classId: string, throwError: boolean = false) {
            patchState(store, { isLoading: true });
            patchState(store, { assessments: [] });
            service.getAssessmentsByClassId(classId).pipe(
                tapResponse({
                    next: (assessments) => {
                        patchState(store, { assessments });
                    },
                    error: (error) => {
                        if (throwError) {
                            errorHandler.handleError(error);
                        }
                    },
                    finalize: () => {
                        patchState(store, { isLoading: false });
                    },
                })
            ).subscribe();
        },

        update(assessment: Assessment) {
            patchState(store, { isLoading: true });
            service.updateAssessment(assessment._id, assessment).pipe(
                tapResponse({
                    next: (updatedAssessment) => {
                        patchState(store, {
                            assessments: store.assessments().map((a) =>
                                a._id === updatedAssessment._id ? updatedAssessment : a
                            ),
                        });
                    },
                    error: (error) => {
                        errorHandler.handleError(error);
                    },
                    finalize: () => {
                        patchState(store, { isLoading: false });
                    },
                })
            ).subscribe();
        },
    })),
    withHooks({
        onInit() {

        },
    })
); 