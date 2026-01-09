import {
  AfterViewInit,
  Component,
  Input,
  input,
  OnChanges,
  OnInit,
  ViewChild,
} from '@angular/core';
import { ChartConfiguration, ChartData } from 'chart.js/auto';

import { BaseChartDirective } from 'ng2-charts';
import { Chart } from 'chart.js';

@Component({
  selector: 'wlk-line-chart-component',
  templateUrl: './line-chart-component.component.html',
  styleUrl: './line-chart-component.component.scss',
  standalone: false
})
export class LineChartComponentComponent implements AfterViewInit, OnChanges, OnInit {
  @ViewChild(BaseChartDirective) chart: BaseChartDirective | undefined;

  uniqueMonths: string[];
  chartLabels: string[];

  public barChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    scales: {
      x: {
        title: {
          display: true,
        },
      },
      y: {
        min: 0,

      },
    },
    plugins: {
      legend: {
        display: true,
      },
    },
  };
  public barChartData: ChartData<'line'> = { labels: [], datasets: undefined };
  @Input() datasets: Array<any> = undefined;
  @Input() labels: Array<number> = [];
  name = input('');
  icon = input('');

  constructor() { }

  parseChartData(): ChartData<'line'> | undefined {
    if (this.datasets) {
      return { labels: this.labels, datasets: this.datasets };
    }
  }

  ngAfterViewInit(): void {
    this.loadData();
  }

  ngOnInit(): void {
    this.loadData();
  }

  labelTransform() {
    return this.labels.map((item) =>
      item
        .toString()
        .slice(0, 6)
        .replace(/(\d{4})(\d{2})/, '$1-$2')
    );
  }

  loadData() {
    const chartData = this.parseChartData();
    if (chartData) {
      this.barChartData = chartData;
      this.chart?.update();

      this.chartLabels = this.labelTransform();
      this.uniqueMonths = [...new Set(this.chartLabels.map((item) => item))];
    }
  }
  ngOnChanges(): void {
    this.loadData();
  }
}
