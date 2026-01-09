import { NgModule } from '@angular/core';
import { CommonModule, NgOptimizedImage } from '@angular/common';
import { CheckedPipe } from './pipes/checked.pipe';
import { YesNoPipe } from './pipes/yes-no.pipe';
import { DateValueAccessorDirective } from './directives/date-value-accessor.directive';
import { DatetimeLocalValueAccessorDirective } from './directives/datetime-local-value-accessor.directive';
import { MatNativeDateModule, MatRippleModule } from '@angular/material/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { Base64ImagePipe } from './pipes/base64-image.pipe';
import { MatPaginator, MatPaginatorIntl } from '@angular/material/paginator';
import { MatPaginationIntlService } from './services/mat-pagination-intl.service';
import { SpinnerComponent } from './modules/spinner/spinner.component';
import { MatProgressSpinner } from '@angular/material/progress-spinner';
import { DeleteTemplateComponent } from './components/delete-dialog/delete-template.component';
import { ToastrModule } from 'ngx-toastr';
import { BarChartComponentComponent } from './modules/bar-chart-component/bar-chart-component.component';
import { PieChartComponentComponent } from './modules/pie-chart-component/pie-chart-component.component';
import { MatIcon, MatIconModule } from '@angular/material/icon';
import { NgChartsModule } from 'ng2-charts';
import { ButtonRippleComponent } from './components/ripple/button-ripple/button-ripple.component';
import { TextFormComponent } from './components/text-form/text-form.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatMenuModule } from '@angular/material/menu';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { FileLoaderComponent } from './components/file-loader/file-loader.component';
import { RateComponent } from './components/rate/rate.component';
import { ImageLoaderComponent } from './components/image-loader/image-loader.component';
import { HighlightDirective } from './directives/highlight.directive';
import { BackComponent } from './components/back/back.component';
import { ProgressBarComponent } from './components/progress-bar/progress-bar.component';
import { LineChartComponentComponent } from './modules/line-chart-component/line-chart-component.component';
const pipes = [CheckedPipe, Base64ImagePipe, YesNoPipe];

const directives = [
  HighlightDirective,
  DateValueAccessorDirective,
  DatetimeLocalValueAccessorDirective,
];

@NgModule({
  declarations: [
    DeleteTemplateComponent,
    SpinnerComponent,
    BarChartComponentComponent,
    PieChartComponentComponent,
    LineChartComponentComponent,
    ButtonRippleComponent,
    TextFormComponent,
    ...pipes,
    ...directives,
    FileLoaderComponent,
    RateComponent,
    ImageLoaderComponent,
    BackComponent,
    ProgressBarComponent,
  ],
  exports: [
    CommonModule,
    ReactiveFormsModule,
    SpinnerComponent,
    TranslateModule,
    ...pipes,
    ...directives,
    DeleteTemplateComponent,
    BarChartComponentComponent,
    ButtonRippleComponent,
    TextFormComponent,
    PieChartComponentComponent,
    FileLoaderComponent,
    RateComponent,
    ImageLoaderComponent,
    BackComponent,
    ProgressBarComponent,
    LineChartComponentComponent,
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    TranslateModule,
    MatNativeDateModule,
    ToastrModule.forRoot(),
    MatDialogModule,
    MatButtonModule,
    MatCardModule,
    MatProgressSpinner,
    NgChartsModule,
    MatRippleModule,
    NgOptimizedImage,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatMenuModule,
    MatPaginator,
    MatSelectModule,
    MatTableModule,
    MatTooltipModule,
    MatExpansionModule,
    MatDatepickerModule,
    MatProgressBarModule,
    TranslateModule,
  ],
  providers: [
    {
      provide: MatPaginatorIntl,
      useClass: MatPaginationIntlService,
    },
    ...pipes,
    ...directives,
  ],
})
export class SharedModule { }
