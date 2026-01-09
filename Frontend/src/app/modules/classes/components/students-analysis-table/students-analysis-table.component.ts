import { Component, effect, input, Input, ViewChild } from '@angular/core';
import { StudentMetrics, ClassMetrics, AssessmentMetrics } from '../../models/class.metrics.model';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
@Component({
  selector: 'wlk-students-analysis-table',
  templateUrl: './students-analysis-table.component.html',
  styleUrl: './students-analysis-table.component.scss',
  standalone: false,
})
export class StudentsAnalysisTableComponent {

  metrics = input<ClassMetrics | null>(null);
  dataSource = new MatTableDataSource<StudentMetrics>([]);
  displayedColumns: string[] = ['name', 'total_writings', 'avg_score', 'avg_grammar_errors', 'pass_rate', 'evolution'];

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor() {

    effect(() => {
      console.log(this.metrics());
      this.dataSource.data = this.metrics()?.student_metrics ?? [];

    });


  }

  getPassRate(element: StudentMetrics) {

    if (element.assessments.count === 0) {
      return 0;
    }



    const passedAssessments = element.assessments.assessments.reduce((acc, assessment) => acc + this.getPassedAssessments(assessment, element.assessments.pass_rate), 0);



    const value = passedAssessments / element.assessments.count;



    return Math.round(value * 100) / 100;


  }


  getPassedAssessments(element: AssessmentMetrics, passRate: number) {
    const value = element.scores.reduce((acc, score) => acc + score.score, 0);
    return value >= passRate ? 1 : 0;
  }

  sumTotalWritings(element: StudentMetrics) {
    return element.assessments.count;
  }

  averageScore(element: StudentMetrics) {

    const totalScore = element.assessments.assessments.reduce((acc, assessment) => acc + assessment.scores.reduce((sum, score) => sum + score.score, 0), 0);

    if (element.assessments.count === 0) {
      return 0;
    }

    const average = totalScore / element.assessments.count;
    return Math.round(average * 100) / 100;
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }



}
