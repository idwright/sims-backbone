import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { HttpClientModule } from '@angular/common/http';

import { MatToolbarModule, MatDialogModule, MatButtonModule } from '@angular/material';
import { MatIconModule } from '@angular/material';
import { MatMenuModule } from '@angular/material';

import { AppRoutingModule } from './app-routing.module';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import 'hammerjs';

import { AppComponent } from './app.component';

import { environment } from '../environments/environment';

import { ReportsComponent } from './reports/reports.component';

import { SimsModule } from '@malariagen/sims';

@NgModule({
  declarations: [
    AppComponent,
    ReportsComponent,
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
      apiLocation: sprocess.env.BACKBONE_API_LOCATION,
      mapsApiKey: sprocess.env.GOOGLE_API_KEY,
      OAuthConfig: {
        'clientId': sprocess.env.CLIENT_ID,
        'redirectUri': sprocess.env.SIMS_REDIRECT_URI,
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
        'responseType': 'code',
        'showDebugInformation': environment.showDebugInformation,
        'dummyClientSecret': sprocess.env.CLIENT_SECRET,
      
      }
    }),
  ],
  providers: [
  ],
  entryComponents: [  
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
