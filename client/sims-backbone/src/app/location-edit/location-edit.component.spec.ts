import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { LocationEditComponent } from './location-edit.component';
import { Component, Input } from '@angular/core';
import { Location, Locations, LocationService, Identifier } from '../typescript-angular-client';
import { FormsModule, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { createAuthServiceSpy, asyncData, createOAuthServiceSpy, ActivatedRouteStub } from '../../testing/index.spec';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { MatFormField } from '@angular/material';
import { HttpTestingController } from '@angular/common/http/testing';
import { OAuthService } from 'angular-oauth2-oidc';
import { MapsAPILoader } from '@agm/core';

import { HttpBackend, HttpClient, HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';


@Component({ selector: 'app-locations-map', template: '' })
class LocationsMapStubComponent {
  @Input() locations: Locations;
  @Input() polygon: any;
  @Input() zoom: number;
}

@Component({ selector: 'app-identifier-table', template: '' })
class IdentifiersTableStubComponent {
  @Input() identifiers;
}

@Component({ selector: 'agm-map', template: '' })
class AgmMapStubComponent {
  @Input() latitude: number;
  @Input() longitude: number;
  @Input() zoom: number;
}

@Component({ selector: 'agm-marker', template: '' })
class AgmMarkerStubComponent {
  @Input() latitude: number;
  @Input() longitude: number;
}

@Component({ selector: 'agm-polygon', template: '' })
class AgmPolygonStubComponent {
  @Input() paths;
}


describe('LocationEditComponent', () => {
  let component: LocationEditComponent;
  let fixture: ComponentFixture<LocationEditComponent>;

  let activatedRoute: ActivatedRouteStub;

  let httpClientSpy: { get: jasmine.Spy };

  let locationService: LocationService;

  let authService;

  let httpClient: HttpClient;
  let httpTestingController: HttpTestingController;

  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({
      latitude: 0,
      longitude: 0
    });

    authService = createAuthServiceSpy();


    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        ReactiveFormsModule,
        RouterModule,
        HttpClientModule,
        HttpClientTestingModule
      ],
      declarations: [
        LocationEditComponent,
        LocationsMapStubComponent,
        IdentifiersTableStubComponent,
        AgmMapStubComponent,
        AgmMarkerStubComponent,
        AgmPolygonStubComponent,
        MatFormField
      ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: LocationService },
        { provide: ActivatedRoute, useValue: activatedRoute },
        MapsAPILoader,

      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {

    // Inject the http service and test controller for each test
    httpClient = TestBed.get(HttpClient);
    httpTestingController = TestBed.get(HttpTestingController);

    fixture = TestBed.createComponent(LocationEditComponent);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should be created', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      let req = backend.expectOne({
        url: 'http://localhost/v1/location/gps/0/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '',
        latitude: 0,
        longitude: 0
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();
      expect(component).toBeTruthy();

    })
  )
  );

  it('should populate edit form', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      let req = backend.expectOne({
        url: 'http://localhost/v1/location/gps/0/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '1234',
        curated_name: 'UK',
        curation_method: 'by hand',
        notes: 'notes',
        country: 'GBR',
        accuracy: 'region',
        latitude: 1,
        longitude: 2,
        identifiers: [<Identifier>{
          identifier_source: 'test_src',
          identifier_type: 'partner_name',
          identifier_value: 'test_val',
          study_name: '9999'
        }, <Identifier>{
          identifier_source: 'test_src',
          identifier_type: 'partner_name',
          identifier_value: 'test_val',
          study_name: '9998'
        }]
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();
      expect(component.locationForm.controls['location_id'].value).toBe(testData.location_id);
      expect(component.locationForm.controls['curated_name'].value).toBe(testData.curated_name);
      expect(component.locationForm.controls['curation_method'].value).toBe(testData.curation_method);
      expect(component.locationForm.controls['notes'].value).toBe(testData.notes);
      expect(component.locationForm.controls['country'].value).toBe(testData.country);
      expect(component.locationForm.controls['accuracy'].value).toBe(testData.accuracy);
      expect(component.locationForm.controls['latitude'].value).toBe(testData.latitude);
      expect(component.locationForm.controls['longitude'].value).toBe(testData.longitude);
      const arrayControls = component.locationForm.controls['identifiers'].value;
      expect(arrayControls[0].identifier_source).toBe(testData.identifiers[0].identifier_source);
      expect(arrayControls[0].identifier_type).toBe(testData.identifiers[0].identifier_type);
      expect(arrayControls[0].identifier_value).toBe(testData.identifiers[0].identifier_value);
      expect(arrayControls[0].study_name).toBe(testData.identifiers[0].study_name);
      expect(arrayControls[1].identifier_source).toBe(testData.identifiers[1].identifier_source);
      expect(arrayControls[1].identifier_type).toBe(testData.identifiers[1].identifier_type);
      expect(arrayControls[1].identifier_value).toBe(testData.identifiers[1].identifier_value);
      expect(arrayControls[1].study_name).toBe(testData.identifiers[1].study_name);
    })
  )
  );

  it('should save edit form', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      let req = backend.expectOne({
        url: 'http://localhost/v1/location/gps/0/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '1234',
        curated_name: 'UK',
        curation_method: 'by hand',
        notes: 'notes',
        country: 'GBR',
        accuracy: 'region',
        latitude: 1,
        longitude: 2,
        identifiers: [<Identifier>{
          identifier_source: 'test_src',
          identifier_type: 'partner_name',
          identifier_value: 'test_val',
          study_name: '9999'
        }, <Identifier>{
          identifier_source: 'test_src',
          identifier_type: 'partner_name',
          identifier_value: 'test_val',
          study_name: '9998'
        }]
      };

      req.flush(testData);

      backend.verify();

      testData.curated_name = 'updated name';
      testData.curation_method = 'for test';
      testData.accuracy = 'city';
      testData.country = 'MLI';
      testData.notes = 'updated';
      component.locationForm.controls['curated_name'].setValue(testData.curated_name);
      component.locationForm.controls['curation_method'].setValue(testData.curation_method);
      component.locationForm.controls['notes'].setValue(testData.notes);
      component.locationForm.controls['country'].setValue(testData.country);
      component.locationForm.controls['accuracy'].setValue(testData.accuracy);

      expect(component.locationForm.valid).toBeTruthy();

      component.onSubmit({
        value: component.locationForm.value,
        valid: component.locationForm.valid
      });

      const put = backend.expectOne({
        url: 'http://localhost/v1/location/' + testData.location_id,
        method: 'PUT'
      });

      put.flush(testData);

      expect(put.request.body.location_id).toBe(testData.location_id);
      expect(put.request.body.curated_name).toBe(testData.curated_name);
      expect(put.request.body.curation_method).toBe(testData.curation_method);
      expect(put.request.body.notes).toBe(testData.notes);
      expect(put.request.body.country).toBe(testData.country);
      expect(put.request.body.accuracy).toBe(testData.accuracy);
      expect(put.request.body.latitude).toBe(testData.latitude);
      expect(put.request.body.longitude).toBe(testData.longitude);
      const arrayControls = put.request.body.identifiers;
      expect(arrayControls[0].identifier_source).toBe(testData.identifiers[0].identifier_source);
      expect(arrayControls[0].identifier_type).toBe(testData.identifiers[0].identifier_type);
      expect(arrayControls[0].identifier_value).toBe(testData.identifiers[0].identifier_value);
      expect(arrayControls[0].study_name).toBe(testData.identifiers[0].study_name);
      expect(arrayControls[1].identifier_source).toBe(testData.identifiers[1].identifier_source);
      expect(arrayControls[1].identifier_type).toBe(testData.identifiers[1].identifier_type);
      expect(arrayControls[1].identifier_value).toBe(testData.identifiers[1].identifier_value);
      expect(arrayControls[1].study_name).toBe(testData.identifiers[1].study_name);

      backend.verify();
    })
  )
  );

  it('should set zoom for country accuracy', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      let req = backend.expectOne({
        url: 'http://localhost/v1/location/gps/0/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '',
        latitude: 0,
        longitude: 0,
        accuracy: 'country'
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      expect(component.locationForm.controls['accuracy'].value).toBe('country');
      expect(component.zoom).toBe(4);

    })
  )
  );

  it('should set zoom for region accuracy', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      let req = backend.expectOne({
        url: 'http://localhost/v1/location/gps/0/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '',
        latitude: 0,
        longitude: 0,
        accuracy: 'region'
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      expect(component.locationForm.controls['accuracy'].value).toBe('region');
      expect(component.zoom).toBe(7);

    })
  )
  );

  it('should set zoom for city accuracy', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      let req = backend.expectOne({
        url: 'http://localhost/v1/location/gps/0/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '',
        latitude: 0,
        longitude: 0,
        accuracy: 'city'
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      expect(component.locationForm.controls['accuracy'].value).toBe('city');
      expect(component.zoom).toBe(11);

    })
  )
  );

  it('should set zoom for building accuracy', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      let req = backend.expectOne({
        url: 'http://localhost/v1/location/gps/0/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '',
        latitude: 0,
        longitude: 0,
        accuracy: 'building'
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      expect(component.locationForm.controls['accuracy'].value).toBe('building');
      expect(component.zoom).toBe(16);

    })
  )
  );

});
