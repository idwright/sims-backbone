import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { HttpClientModule } from '@angular/common/http';

import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';

import { AppRoutingModule } from './app-routing.module';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import 'hammerjs';

import { AppComponent } from './app.component';

import { environment } from '../environments/environment';

import { ReportsComponent } from './reports/reports.component';

import { SimsModule } from '@malariagen/sims';
import { OAuthStorage } from 'angular-oauth2-oidc';
import { AlfStudyDetailComponent } from './alf-study-detail/alf-study-detail.component';

export function storageFactory(): OAuthStorage {
  return localStorage
}

@NgModule({
  declarations: [
    AppComponent,
    ReportsComponent,
    AlfStudyDetailComponent
  ],
  imports: [
    BrowserModule,
    MatToolbarModule,
    MatIconModule,
    MatMenuModule,
    MatDialogModule,
    MatButtonModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    SimsModule.forRoot({
      apiLocation: environment.apiLocation,
      mapsApiKey: environment.mapsApiKey,
      OAuthConfig: {
        'clientId': environment.clientId,
        'redirectUri': environment.redirectUri,
        'postLogoutRedirectUri': environment.postLogoutRedirectUri,
        'loginUrl': environment.loginUrl,
        'scope': environment.scope,
        'resource': '',
        'rngUrl': '',
        'oidc': false,
        'requestAccessToken': true,
        'options': null,
        'clearHashAfterLogin': true,
        'tokenEndpoint': environment.tokenEndpoint,
        'responseType': 'token',
        'showDebugInformation': environment.showDebugInformation,
        'dummyClientSecret': environment.dummyClientSecret
      }
    }),
  ],
  providers: [
    //{ provide: OAuthModuleConfig, useValue: authModuleConfig },
    { provide: OAuthStorage, useFactory: storageFactory },
  ],
  entryComponents: [
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
