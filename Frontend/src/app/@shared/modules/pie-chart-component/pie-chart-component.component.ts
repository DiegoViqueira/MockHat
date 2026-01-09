import { Component, Input, input, ViewChild } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartData, ChartType } from 'chart.js/auto';
import { Chart } from 'chart.js';

@Component({
    selector: 'wlk-pie-chart-component',
    templateUrl: './pie-chart-component.component.html',
    styleUrl: './pie-chart-component.component.scss',
    standalone: false
})
export class PieChartComponentComponent {
  @ViewChild(BaseChartDirective) chart: BaseChartDirective | undefined;
  private readonly graphColor = ['#5882FA', '#BCA9F5'];
  public barChartOptions: ChartConfiguration['options'] = {
    responsive: true,

    plugins: {
      legend: {
        display: true,
        position: 'right', // Positions: 'top', 'left', 'bottom', 'right'
        align: 'center', // Alignment: 'start', 'center', 'end'
      },
    },
  };

  public barChartData: ChartData<'doughnut'> = {
    labels: [],
    datasets: [],
  };
  @Input() datasets: Array<any> = [];
  @Input() labels: Array<number> = [];
  name = input('');
  icon = input('');

  constructor() {
    Chart.defaults.datasets.doughnut.backgroundColor = this.graphColor;
  }

  parseChartData(): ChartData<'doughnut'> | undefined {
    if (this.datasets) {
      return { labels: this.labels, datasets: this.datasets };
    }
  }

  ngAfterViewInit(): void {
    const chartData = this.parseChartData();
    if (chartData) {
      this.barChartData = chartData;
      this.chart?.update();
    }
  }

  ngOnInit(): void {
    const chartData = this.parseChartData();
    if (chartData) {
      this.barChartData = chartData;
      this.chart?.update();
    }
  }

  ngOnChanges(): void {
    const chartData = this.parseChartData();
    if (chartData) {
      this.barChartData = chartData;
      this.chart?.update();
    }
  }
}
