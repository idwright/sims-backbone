import { Component, OnInit, AfterViewInit, ViewChild, ChangeDetectorRef, Input, ChangeDetectionStrategy } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatTable } from '@angular/material/table';
import { DerivativeSample } from '../typescript-angular-client';
import { Observable } from 'rxjs';
import { DerivativeSamplesService } from '../derivative-samples.service';
import { DerivativeSamplesSource } from '../derivative-sample.datasource';
import { tap } from 'rxjs/operators';
import { DerivativeSampleService } from '../typescript-angular-client/api/derivativeSample.service';

@Component({
  selector: 'sims-ds-list',
  templateUrl: './ds-list.component.html',
  styleUrls: ['./ds-list.component.scss'],
  providers: [DerivativeSamplesService, DerivativeSampleService],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DsListComponent implements OnInit, AfterViewInit {

  _dataSource: DerivativeSamplesSource;

  displayedColumns = [];

  _studyName: string;
  _eventSetName: string;

  _pageSize: number = 25;
  
  @Input()
  filter: string;

  @ViewChild(MatPaginator, { static: false }) paginator: MatPaginator;
  @ViewChild(MatTable, { static: true }) table;

  selectedEvents = new Set<string>();

  @Input()
  downloadFileName = 'data.csv';

  @Input()
  jsonDownloadFileName = 'data.json';

  constructor(private changeDetector: ChangeDetectorRef, private derivativeSamplesService: DerivativeSamplesService) { }

  ngOnInit(): void {

    this._dataSource = new DerivativeSamplesSource(this.derivativeSamplesService);

    // Recalcuate the column headers when the data changes
    const obs: Observable<DerivativeSample[]> = this._dataSource.connect(this.table);

    obs.subscribe({
      next: sevents => this.defineColumnHeaders(sevents),
      error(msg) {
        console.log(msg);
      },
      complete() {
        console.log('complete');
      }
    });

    this._dataSource.loadDerivativeSamples(this.filter, 'asc', 0, 50);

  }

  ngAfterViewInit() {

    if (this.paginator) {
      this.paginator.page
        .pipe(
          tap(() => this.loadOriginalSamplesPage())
        )
        .subscribe();
    }

  }

  @Input()
  set studyName(studyName: string) {
    this._studyName = studyName;
    this.downloadFileName = studyName + '_derivative_samples.csv';
    this.jsonDownloadFileName = studyName + '_derivative_samples.json';
  }

  loadOriginalSamplesPage() {
    this._dataSource.loadDerivativeSamples(this.filter,
      'asc',
      this.paginator.pageIndex,
      this.paginator.pageSize
    );

  }

  defineColumnHeaders(derivativeSamples) {

    if (derivativeSamples === undefined) {
      return;
    }

    let columnsForDisplay = ['derivative_sample_id', 'study_name', 'dna_prep', 'taxon', 'partner_species'];
    columnsForDisplay = columnsForDisplay.concat(this._dataSource.attrTypes);
    columnsForDisplay = columnsForDisplay.concat(['original_sample_id']);

    if (columnsForDisplay !== this.displayedColumns) {
      this.displayedColumns = columnsForDisplay;
      this.changeDetector.markForCheck();
    }

  }


}
