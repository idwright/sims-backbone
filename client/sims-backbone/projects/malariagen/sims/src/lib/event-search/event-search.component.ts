import { Component, OnInit } from '@angular/core';
import { SamplingEventService } from '../typescript-angular-client/api/samplingEvent.service';
import { MetadataService } from '../typescript-angular-client/api/metadata.service';
import { OriginalSampleService } from '../typescript-angular-client/api/originalSample.service';
import { DerivativeSampleService } from '../typescript-angular-client/api/derivativeSample.service';
import { AssayDataService } from '../typescript-angular-client/api/assayData.service';

import { SamplingEvents } from '../typescript-angular-client/model/samplingEvents';
import { AssayData, OriginalSamples, DerivativeSamples } from '../typescript-angular-client';


@Component({
  selector: 'sims-event-search',
  providers: [
    SamplingEventService, MetadataService,
    OriginalSampleService, DerivativeSampleService, AssayDataService],
  templateUrl: './event-search.component.html',
  styleUrls: ['./event-search.component.scss']
})
export class EventSearchComponent implements OnInit {

  originalSamples: OriginalSamples;
  samplingEvents: SamplingEvents;
  derivativeSamples: DerivativeSamples;
  assayData: AssayData;
  attr_type: string;
  attr_value: string;

  options: string[];

  constructor(private sampleService: SamplingEventService, private metadataService: MetadataService,
    private originalSampleService: OriginalSampleService,
    private derivativeSampleService: DerivativeSampleService, private assayDataService: AssayDataService) { }

  ngOnInit() {

    this.metadataService.getAttrTypes().subscribe(attrTypes => {
      this.options = attrTypes;
    });
    this.warmUp();

    this.attr_type = 'roma_id';
    //this.attrValue = 'QS0167-C';
    this.search();

  }

  warmUp() {
    this.sampleService.downloadSamplingEventsByOsAttr('', '').subscribe();
    this.originalSampleService.downloadOriginalSamplesByAttr('', '').subscribe();
    this.derivativeSampleService.downloadDerivativeSamplesByOsAttr('', '').subscribe();
    this.assayDataService.downloadAssayDataByOsAttr('', '').subscribe();
  }

  search() {
    if (this.attr_type && this.attr_value) {
      this.sampleService.downloadSamplingEventsByOsAttr(this.attr_type, this.attr_value).subscribe(samplingEvents => {
        this.samplingEvents = samplingEvents;
      });
      this.originalSampleService.downloadOriginalSamplesByAttr(this.attr_type, this.attr_value).subscribe(originalSamples => {
        this.originalSamples = originalSamples;

        this.derivativeSampleService.downloadDerivativeSamplesByOsAttr(this.attr_type, this.attr_value).subscribe(derivativeSamples => {
          this.derivativeSamples = derivativeSamples;

          this.assayDataService.downloadAssayDataByOsAttr(this.attr_type, this.attr_value).subscribe(assayData => {
            this.assayData = assayData;
          });
        });
      });

    }
  }
}
