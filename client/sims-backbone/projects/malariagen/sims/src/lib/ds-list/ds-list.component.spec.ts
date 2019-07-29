import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DsListComponent } from './ds-list.component';
import { OverlayModule } from '@angular/cdk/overlay';
import { MatTableModule, MatTooltipModule, MatPaginatorModule } from '@angular/material';
import { HttpClientModule } from '@angular/common/http';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { DerivativeSampleDisplayPipe } from '../derivative-sample-display.pipe';
import { createOAuthServiceSpy } from '../../testing/index.spec';
import { DerivativeSampleService } from '../typescript-angular-client';
import { OAuthService } from 'angular-oauth2-oidc';
import { DerivativeSamplesService } from '../derivative-samples.service';
import { MockComponent } from 'ng-mocks';
import { DownloaderDsCsvComponent } from '../downloader-ds-csv/downloader-ds-csv.component';
import { DownloaderDsJsonComponent } from '../downloader-ds-json/downloader-ds-json.component';

describe('DsListComponent', () => {
  let component: DsListComponent;
  let fixture: ComponentFixture<DsListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({     imports: [
      OverlayModule,
      MatTableModule,
      MatPaginatorModule,
      MatTooltipModule,
      HttpClientModule,
      HttpClientTestingModule,
      NoopAnimationsModule
    ],
    declarations: [ 
      DsListComponent,
      MockComponent(DownloaderDsCsvComponent),
      MockComponent(DownloaderDsJsonComponent),
      DerivativeSampleDisplayPipe, 
    ],
    providers: [
      { provide: OAuthService, useValue: createOAuthServiceSpy() },
      { provide: DerivativeSampleService },
      { provide: DerivativeSamplesService },
    ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
