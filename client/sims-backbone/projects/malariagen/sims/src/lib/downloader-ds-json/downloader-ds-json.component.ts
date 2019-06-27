import { Component, OnInit, Input } from '@angular/core';
import { DerivativeSamplesSource } from '../derivative-sample.datasource';
import { BehaviorSubject, Observable } from 'rxjs';
import { DerivativeSampleDisplayPipe } from '../derivative-sample-display.pipe';
import { DerivativeSamplesService } from '../derivative-samples.service';
import { DerivativeSample, DerivativeSamples } from '../typescript-angular-client';
import { CollectionViewer } from '@angular/cdk/collections';

import * as FileSaver from 'file-saver';
import { DerivativeSampleService } from '../typescript-angular-client/api/derivativeSample.service';

@Component({
  selector: 'sims-downloader-ds-json',
  templateUrl: './downloader-ds-json.component.html',
  styleUrls: ['./downloader-ds-json.component.scss'],
  providers: [DerivativeSamplesService, DerivativeSampleService, DerivativeSampleDisplayPipe],
})
export class DownloaderDsJsonComponent implements CollectionViewer {

  derivativeSamples: DerivativeSamples;
  header = false;
  separator = '\t';
  csvString = '';
  pageSize = 1000;
  pageNumber = 0;

  _dataSource: DerivativeSamplesSource;
  viewChange = new BehaviorSubject<{ start: number, end: number }>({ start: 0, end: Number.MAX_VALUE });

  @Input()
  fileName = 'data.csv';
  @Input()
  filter: string;
  @Input()
  downloaderName = 'Download JSON';
  @Input()
  headers: string[] = [];

  constructor(private displayPipe: DerivativeSampleDisplayPipe, private derivativeSamplesService: DerivativeSamplesService) {

    this._dataSource = new DerivativeSamplesSource(this.derivativeSamplesService);

    const obs: Observable<DerivativeSample[]> = this._dataSource.connect(this);


    obs.subscribe({
      next: sevent => this.extractEvents(sevent),
      error(msg) {
        console.log(msg);
      },
      complete() {
        console.log('complete');
      }
    });

  }

  build() {

    this.pageNumber = 0;

    this._dataSource.loadDerivativeSamples(this.filter, 'asc', this.pageNumber, this.pageSize);

  }

  extractEvents(d: Array<DerivativeSample>) {

    if (d.length === 0) {
      return;
    }

    if (this.pageNumber === 0) {
      this.derivativeSamples = <DerivativeSamples>{};
      this.derivativeSamples.derivative_samples = [];
    }

    this.derivativeSamples.derivative_samples = this.derivativeSamples.derivative_samples.concat(d);


    if ((this.pageNumber + 1) * this.pageSize < this._dataSource.derivativeSampleCount) {
      this.pageNumber++;
      this._dataSource.loadDerivativeSamples(this.filter, 'asc', this.pageNumber, this.pageSize);
    } else {
      // this.derivativeSamples.attrTypes = this._dataSource.attrTypes;
      this.derivativeSamples.count = this._dataSource.derivativeSampleCount;
      this.buildDownloader(JSON.stringify(this.derivativeSamples));
    }

  }
  private buildDownloader(data) {

    const blob = new Blob([data], { type: 'application/json;charset=utf-8' });

    FileSaver.saveAs(blob, this.fileName);

  }

}
