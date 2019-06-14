import { Component, OnInit, ViewChild, ChangeDetectorRef, Input, AfterViewInit, ChangeDetectionStrategy } from '@angular/core';
import { OriginalSamplesService } from '../original-samples.service';
import { MatPaginator, MatTable, MatDialog } from '@angular/material';
import { Observable } from 'rxjs';
import { OriginalSample, OriginalSampleService } from '../typescript-angular-client';
import { tap } from 'rxjs/operators';
import { OriginalSamplesSource } from '../original-sample.datasource';

@Component({
  selector: 'sims-os-list',
  templateUrl: './os-list.component.html',
  styleUrls: ['./os-list.component.scss'],
  providers: [OriginalSamplesService, OriginalSampleService],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OsListComponent implements OnInit, AfterViewInit {

  _dataSource: OriginalSamplesSource;

  displayedColumns = [];

  _studyName: string;
  _eventSetName: string;

  _pageSize: number = 25;

  @Input()
  filter: string;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatTable) table;

  selectedEvents = new Set<string>();

  @Input()
  downloadFileName = 'data.csv';

  @Input()
  jsonDownloadFileName = 'data.json';

  constructor(private changeDetector: ChangeDetectorRef, private originalSamplesService: OriginalSamplesService) { }

  ngOnInit(): void {

    this._dataSource = new OriginalSamplesSource(this.originalSamplesService);

    // Recalcuate the column headers when the data changes
    const obs: Observable<OriginalSample[]> = this._dataSource.connect(this.table);

    obs.subscribe({
      next: sevents => this.defineColumnHeaders(sevents),
      error(msg) {
        console.log(msg);
      },
      complete() {
        console.log('complete');
      }
    });

    this._dataSource.loadOriginalSamples(this.filter, 'asc', 0, 50);

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
    this.downloadFileName = studyName + '_original_samples.csv';
    this.jsonDownloadFileName = studyName + '_original_samples.json';
  }

  loadOriginalSamplesPage() {
    this._dataSource.loadOriginalSamples(this.filter,
      'asc',
      this.paginator.pageIndex,
      this.paginator.pageSize
    );

  }

  defineColumnHeaders(originalSamples) {

    if (originalSamples === undefined) {
      return;
    }

    let columnsForDisplay = ['original_sample_id', 'study_id', 'partner_species', 'taxa', 'doc'];
    columnsForDisplay = columnsForDisplay.concat(this._dataSource.attrTypes);
    columnsForDisplay = columnsForDisplay.concat(['sampling_event_id']);

    if (columnsForDisplay !== this.displayedColumns) {
      this.displayedColumns = columnsForDisplay;
      this.changeDetector.markForCheck();
    }

  }


}
