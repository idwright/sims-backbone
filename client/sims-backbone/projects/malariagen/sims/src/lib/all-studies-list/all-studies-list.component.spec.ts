import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { asyncData } from '../../testing/index.spec';

import { AllStudiesListComponent } from './all-studies-list.component';
import { StudyService } from '../typescript-angular-client';
import { OAuthService } from 'angular-oauth2-oidc';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs/observable/of';
import { MockComponent } from 'ng-mocks';
import { StudiesListComponent } from '../studies-list/studies-list.component';

describe('AllStudiesListComponent', () => {
  let component: AllStudiesListComponent;
  let fixture: ComponentFixture<AllStudiesListComponent>;
  let httpClientSpy: { get: jasmine.Spy };
  let studyService: StudyService;

  beforeEach(async(() => {

    // Create a fake AuthService object 
    const authService = jasmine.createSpyObj('OAuthService', ['getAccessToken', 'getConfiguration']);
    // Make the spy return a synchronous Observable with the test data
    let getAccessToken = authService.getAccessToken.and.returnValue(of(undefined));
    let getConfiguration = authService.getConfiguration.and.returnValue(of(undefined));

    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);
    studyService = new StudyService(<any>httpClientSpy, '', authService.getConfiguration());

    TestBed.configureTestingModule({
      declarations: [
        AllStudiesListComponent,
        MockComponent(StudiesListComponent)
      ],
      providers: [
        { provide: OAuthService, useValue: authService },
        { provide: HttpClient, useValue: httpClientSpy },
        { provide: StudyService, useValue: studyService }
      ]
    })
      .compileComponents();

    httpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AllStudiesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('should have requested all studies', () => {
    expect(httpClientSpy.get.calls.first().args[0]).toBe('http://localhost/v1/studies', 'url');
    expect(httpClientSpy.get.calls.count()).toBe(1, 'one call');
  });
});
