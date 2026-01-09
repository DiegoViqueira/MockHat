import { MatDialogConfig } from '@angular/material/dialog';
import { Level } from '../../modules/users/models/user-level.enum';
import { Section } from '../../modules/shared/models/section.enum';
import { Institution } from '../../modules/shared/models/institutions.enum';
import { ExamType } from '../../modules/shared/models/exam_type.enum';
import { WritingTask } from '../../modules/assessments/models/writing.task.model';
import { UserPlan } from '../../modules/users/models/plan.enum';
export const tablePageSizes = [25, 50, 100];
export const passwordPattern =
  '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[^A-Za-z0-9]).{8,}$';

export const emailPattern = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$';

//export const levels = [Level.A0, Level.A1, Level.A2, Level.B1, Level.B2, Level.C1, Level.C2];
export const levels = [Level.B1, Level.B2, Level.C1, Level.C2, Level.EBAU];

export enum PlanGroup {
  BUSINESS = 'business',
  INDIVIDUAL = 'individual',
}

export const plans = {
  [PlanGroup.BUSINESS]: { group: PlanGroup.BUSINESS, plans: [UserPlan.BUSINESS, UserPlan.BUSINESS_PRO] },
  [PlanGroup.INDIVIDUAL]: { group: PlanGroup.INDIVIDUAL, plans: [UserPlan.FREE, UserPlan.BASIC, UserPlan.PREMIUM] },
}


export const InstitutionsExamTypesTasksByLevel = {
  [Institution.CAMBRIDGE]: {
    [ExamType.CEQ]: [
      { level: Level.B1, tasks: [WritingTask.EMAIL, WritingTask.ARTICLE, WritingTask.STORY] },
      {
        level: Level.B2, tasks: [WritingTask.ESSAY,
        WritingTask.ARTICLE,
        WritingTask.EMAIL,
        WritingTask.REPORT,
        WritingTask.REVIEW,
        WritingTask.STORY,
        ]
      },
      {
        level: Level.C1, tasks: [WritingTask.ESSAY,
        WritingTask.EMAIL,
        WritingTask.PROPOSAL,
        WritingTask.REPORT,
        WritingTask.REVIEW,]
      },
      {
        level: Level.C2, tasks: [WritingTask.ESSAY,
        WritingTask.ARTICLE,
        WritingTask.REVIEW,
        WritingTask.LETTER,
        ]
      }
    ],

  },
  [Institution.BACHILLERATO]: {
    [ExamType.EBAU]: [WritingTask.FOR_AND_AGAINST_ESSAY, WritingTask.FORMAL_APPLICATION_EMAIL, WritingTask.FORMAL_COMPLAINT_EMAIL, WritingTask.INFORMAL_EMAIL, WritingTask.OPINION_ESSAY],
  },
};
export const TaskByLevel = [
  {
    level: Level.EBAU,
    tasks: [WritingTask.FOR_AND_AGAINST_ESSAY, WritingTask.FORMAL_APPLICATION_EMAIL, WritingTask.FORMAL_COMPLAINT_EMAIL, WritingTask.INFORMAL_EMAIL, WritingTask.OPINION_ESSAY],
  },
  {
    level: Level.B1,
    tasks: [WritingTask.EMAIL, WritingTask.ARTICLE, WritingTask.STORY],
  },
  {
    level: Level.B2,
    tasks: [
      WritingTask.ESSAY,
      WritingTask.ARTICLE,
      WritingTask.EMAIL,
      WritingTask.REPORT,
      WritingTask.REVIEW,
      WritingTask.STORY,
    ],
  },
  {
    level: Level.C1,
    tasks: [
      WritingTask.ESSAY,
      WritingTask.EMAIL,
      WritingTask.PROPOSAL,
      WritingTask.REPORT,
      WritingTask.REVIEW,
    ],
  },
  {
    level: Level.C2,
    tasks: [
      WritingTask.ESSAY,
      WritingTask.ARTICLE,
      WritingTask.REVIEW,
      WritingTask.LETTER,
    ],
  },
];

export const writingTasks = [WritingTask.EMAIL, WritingTask.ARTICLE, WritingTask.LETTER, WritingTask.STORY, WritingTask.FOR_AND_AGAINST_ESSAY, WritingTask.FORMAL_APPLICATION_EMAIL, WritingTask.FORMAL_COMPLAINT_EMAIL, WritingTask.INFORMAL_EMAIL, WritingTask.OPINION_ESSAY];
export const sections = [
  Section.READING,
  Section.LISTENING,
  Section.SPEAKING,
  Section.WRITING,
  Section.USE_OF_ENGLISH,
];

export const institutions = [Institution.CAMBRIDGE, Institution.BACHILLERATO];
export const examTypes = [ExamType.CEQ, ExamType.IELTS, ExamType.LINGUA_SKILL, ExamType.EBAU];

export function dialogConfigFactory<T>(
  custom: { data?: T; width?: string; height?: string } = {}
): MatDialogConfig {
  return {
    disableClose: true,
    autoFocus: true,
    hasBackdrop: true,
    height: 'auto',
    width: 'auto',
    ...custom,
  } as MatDialogConfig;
}

export function getBase64(file: File) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      const content = reader.result as string;
      resolve(content.split(',').pop());
    };
    reader.onprogress = () => { };
    reader.onerror = (error) => reject(error);
  });
}

export interface TaskConfig {
  level: Level;
  tasks: WritingTask[];
}

export interface ExamTypeConfig {
  examType: ExamType;
  levels: TaskConfig[];
}

export interface InstitutionConfig {
  institution: Institution;
  examTypes: ExamTypeConfig[];
}



export const WritingConfiguration: InstitutionConfig[] = [
  {
    institution: Institution.CAMBRIDGE,
    examTypes: [
      {
        examType: ExamType.CEQ,
        levels: [
          {
            level: Level.B1,
            tasks: [WritingTask.EMAIL, WritingTask.ARTICLE, WritingTask.STORY]
          },
          {
            level: Level.B2,
            tasks: [
              WritingTask.ESSAY,
              WritingTask.ARTICLE,
              WritingTask.EMAIL,
              WritingTask.REPORT,
              WritingTask.REVIEW,
              WritingTask.STORY,
            ]
          },
          {
            level: Level.C1,
            tasks: [
              WritingTask.ESSAY,
              WritingTask.EMAIL,
              WritingTask.PROPOSAL,
              WritingTask.REPORT,
              WritingTask.REVIEW,
            ]
          },
          {
            level: Level.C2,
            tasks: [
              WritingTask.ESSAY,
              WritingTask.ARTICLE,
              WritingTask.REVIEW,
              WritingTask.LETTER,
            ],
          },
        ]
      }
    ]
  },
  {
    institution: Institution.BACHILLERATO,
    examTypes: [
      {
        examType: ExamType.EBAU,
        levels: [
          {
            level: Level.EBAU,
            tasks: [WritingTask.FOR_AND_AGAINST_ESSAY, WritingTask.FORMAL_APPLICATION_EMAIL, WritingTask.FORMAL_COMPLAINT_EMAIL, WritingTask.INFORMAL_EMAIL, WritingTask.OPINION_ESSAY]
          }
        ]
      }
    ]
  }
];

export function getLevelsByInstitution(institution: Institution): Level[] {
  const institutionConfig = WritingConfiguration.find(config => config.institution === institution);
  return institutionConfig?.examTypes.flatMap(examType => examType.levels.map(level => level.level)) || [];
}

// Helper functions para filtrar
export function getExamTypesByInstitution(institution: Institution): ExamType[] {
  const institutionConfig = WritingConfiguration.find(config => config.institution === institution);
  return institutionConfig?.examTypes.map(examType => examType.examType) || [];
}

export function getLevelsByInstitutionAndExamType(
  institution: Institution,
  examType: ExamType
): Level[] {
  const institutionConfig = WritingConfiguration.find(config => config.institution === institution);
  const examTypeConfig = institutionConfig?.examTypes.find(config => config.examType === examType);
  return examTypeConfig?.levels.map(level => level.level) || [];
}

export function getTasksByInstitutionExamTypeAndLevel(
  institution: Institution,
  examType: ExamType,
  level: Level
): WritingTask[] {
  const institutionConfig = WritingConfiguration.find(config => config.institution === institution);
  const examTypeConfig = institutionConfig?.examTypes.find(config => config.examType === examType);
  const levelConfig = examTypeConfig?.levels.find(config => config.level === level);
  return levelConfig?.tasks || [];
}
