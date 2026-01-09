


export interface ScoreTrend {
    weekly_average_scores: Record<string, number>;
}

export interface ScoreHistogram {
    histogram: number[];
    bin_edges: number[];
}

export interface ScoreErrorCorrelation {
    correlation: number;
    scores: number[];
    errors: number[];
}


export interface CriteriaAverage {
    criteria_scores: Record<string, number>;
}


export interface CriteriaDistribution {
    criteria_stats: Record<string, Record<string, number>>;
}

export interface ClassScoreMetrics {
    average_score: number;
    pass_rate: number;
    avg_grammar_errors: number;
}

export interface ClassMetrics {
    score_histogram: ScoreHistogram;
    score_trends: ScoreTrend;
    criteria_distribution: CriteriaDistribution;
    criteria_average: CriteriaAverage;
    class_score_metrics: ClassScoreMetrics;
    score_error_correlation: ScoreErrorCorrelation;
    student_metrics: StudentMetrics[];
}


export class ScoreEntry {
    criteria: string = "";
    score: number = 0;
}

export class AssessmentMetrics {
    date: string = "";
    scores: ScoreEntry[] = [];
    grammar_errors: number = 0;
}

export class AssessmentsMetrics {
    assessments: AssessmentMetrics[] = [];
    count: number = 0;
    score_average: number = 0;
    grammar_errors_average: number = 0;
    pass_rate: number = 0;
}


export class StudentMetrics {
    name: string = "";
    assessments: AssessmentsMetrics = new AssessmentsMetrics();
}
