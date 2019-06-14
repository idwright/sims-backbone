import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'sims-study-os-list',
  templateUrl: './study-os-list.component.html',
  styleUrls: ['./study-os-list.component.scss']
})
export class StudyOsListComponent implements OnInit {

  studyName: string;
  
  filter: string;

  downloadFileName: string;

  jsonDownloadFileName: string;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.studyName = pmap.get('studyName');
    });
    this.filter = 'studyId:' + this.studyName;
    this.downloadFileName = 'original_samples_study_' + this.studyName + '.csv';
    this.jsonDownloadFileName = 'original_samples_study_' + this.studyName + '.json';
  }
}
