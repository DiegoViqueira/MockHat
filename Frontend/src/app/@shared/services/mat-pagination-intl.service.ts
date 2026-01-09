import { Injectable } from '@angular/core';
import { MatPaginatorIntl } from '@angular/material/paginator';
import { TranslateService } from '@ngx-translate/core';

/**
 * Utility service necessary to translate the mat-paginator
 * References:
 * https://material.angular.io/components/paginator/overview
 * https://stackoverflow.com/questions/46869616/how-to-use-matpaginatorintl
 */
@Injectable()
export class MatPaginationIntlService extends MatPaginatorIntl {
  constructor(private translate: TranslateService) {
    super();

    // React whenever the language is changed
    this.translate.onLangChange.subscribe(() => this.translateLabels());

    // Initialize the translations once at construction time
    this.translateLabels();
  }

  getRangeLabel = (page: number, pageSize: number, length: number): string => {
    const of = this.translate ? this.translate.instant('paginator.of') : 'of';
    if (length === 0 || pageSize === 0) {
      return '0 ' + of + ' ' + length;
    }
    length = Math.max(length, 0);
    const startIndex =
      page * pageSize > length
        ? (Math.ceil(length / pageSize) - 1) * pageSize
        : page * pageSize;

    const endIndex = Math.min(startIndex + pageSize, length);
    return startIndex + 1 + ' - ' + endIndex + ' ' + of + ' ' + length;
  };

  injectTranslateService(translate: TranslateService): void {
    this.translate = translate;

    this.translate.onLangChange.subscribe(() => {
      this.translateLabels();
    });

    this.translateLabels();
  }

  translateLabels(): void {
    this.firstPageLabel = this.translate.instant('paginator.firstPage');
    this.itemsPerPageLabel = this.translate.instant('paginator.itemsPerPage');
    this.lastPageLabel = this.translate.instant('paginator.lastPage');
    this.nextPageLabel = this.translate.instant('paginator.nextPage');
    this.previousPageLabel = this.translate.instant('paginator.previousPage');
    this.changes.next(); // Fire a change event to make sure that the labels are refreshed
  }
}
