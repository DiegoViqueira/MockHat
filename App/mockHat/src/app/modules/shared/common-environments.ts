import { Level } from "../models/user-level.enum";
import { WritingTask } from "../models/writing.task.model";

export const levels = [Level.B1, Level.B2, Level.C1];

export const TaskByLevel = [
    {
        level: Level.B1,
        tasks: [WritingTask.Email, WritingTask.Article, WritingTask.Story],
    },
    {
        level: Level.B2,
        tasks: [
            WritingTask.Essay,
            WritingTask.Article,
            WritingTask.Email,
            WritingTask.Report,
            WritingTask.Review,
            WritingTask.Story,
        ],
    },
    {
        level: Level.C1,
        tasks: [
            WritingTask.Essay,
            WritingTask.Email,
            WritingTask.Proposal,
            WritingTask.Report,
            WritingTask.Review,
        ],
    },
];
