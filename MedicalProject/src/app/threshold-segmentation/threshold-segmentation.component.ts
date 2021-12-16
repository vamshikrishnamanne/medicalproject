import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-threshold-segmentation',
  templateUrl: './threshold-segmentation.component.html',
  styleUrls: ['./threshold-segmentation.component.scss']
})
export class ThresholdSegmentationComponent implements OnInit {
  
  threshold: any;
  isShown: boolean = false;
  constructor(private http: HttpClient) {

  }

  ngOnInit(): void {
  }

fileData!: File 
fileUploadProgress!: string 


 
fileProgress(fileInput: any) {
      this.fileData = <File>fileInput.target.files[0];
      
}
 
createImageFromBlob(image: Blob) {
  let reader = new FileReader();
  reader.addEventListener("load", () => {
     this.threshold = reader.result;
  }, false);

  if (image) {
     reader.readAsDataURL(image);
  }
 }
 
onSubmit() {

  var  formData = new FormData();
  formData.append('file',this.fileData, this.fileData.name );
this.http.post('http://127.0.0.1:5000/binarize',  formData,{ responseType: 'blob' })
 .subscribe((baseImage : any) => {
  this.createImageFromBlob(baseImage);
 this.isShown = true
});

 }
}


