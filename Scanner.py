import numpy as np
import cv2
import os
import re
import boto3
# from scipy.special import sc
import scipy.special
from scipy import special


class AdharExtract:
        def getData(self,img1,img2):
                image=cv2.imread(img1)   #read in the image
                image=cv2.resize(image,(1000,800)) #resizing because opencv does not work well with bigger images
                orig=image.copy()
                gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  #RGB To Gray Scale
                blurred=cv2.GaussianBlur(gray,(5,5),0)  #(5,5) is the kernel size and 0 is sigma that determines the amount of blur
                 #storing processed image temporarily
                cv2.imwrite('processed_image.png',blurred)


                image=cv2.imread(img2)   #read in the image
                image=cv2.resize(image,(1000,800)) #resizing because opencv does not work well with bigger images
                orig=image.copy()
                gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  #RGB To Gray Scale
                blurred=cv2.GaussianBlur(gray,(5,5),0)  #(5,5) is the kernel size and 0 is sigma that determines the amount of blur
                 #storing processed image temporarily
                cv2.imwrite('processed_image1.png',blurred)
                client = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id='Key',aws_secret_access_key='Key')
                client1 = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id='Key',aws_secret_access_key='Key')

                with open("processed_image.png", "rb") as imageFile:
                        response=client.detect_text(Image={'Bytes': imageFile.read()})

                with open("processed_image1.png", "rb") as imageFile:
                        response1=client1.detect_text(Image={'Bytes': imageFile.read()})


                        textDetections1=response1['TextDetections']

                        for text in textDetections1:
                                print('Detected text:' + text['DetectedText'])

                        address=""
                        a=[]
                        for text in textDetections1:
                                if(text['Confidence']>85 and text['Type']=="LINE" ):
                                        a.append(text['DetectedText'])

                                #print(text['DetectedText'])
                        for i in range(len(a)):
                                if((a[i]=='Address:') or (a[i]=='Address :') or (a[i]=='Address') or (a[i]=='Address ')):
                                        while(1):
                                                address=address+a[i+1]
                                                i=i+1
                                                if((a[i+1]=='www') or (a[i+1]=='wwW') or (a[i+1]=='wWW') or (a[i+1]=='WWW')  or (a[i+1]=='wWw')):
                                                        break


                        textDetections=response['TextDetections']
                        # print ('Detected text')
                        name,gender,aadhar_no,mobile_no,DoB="","","","",""
                        for text in textDetections:
                                print('Detected text:' + text['DetectedText'])

                                #following is logic to extract details

                                if(text['Confidence']>85):
                                        if(text['Type']=='LINE' and re.search(r'\w* \w*',text['DetectedText'])):
                                                if('DOB' in text['DetectedText'] or 'DOB' in text['DetectedText']):
                                                        print('Date of Birth:',text['DetectedText'][text['DetectedText'].find('DOB')+5:])
                                                        DoB1=text['DetectedText'][text['DetectedText'].find('DOB')+5:]
                                                        if(DoB1!=""):
                                                                DoB=DoB1
                                        if('MALE' in text['DetectedText'] or 'Male' in text['DetectedText']  ):
                                                        print("Gender: Male")
                                                        gender="Male"
                                        elif('FEMALE' in text['DetectedText'] or 'Female' in text['DetectedText']):
                                                        print("Gender: Female")
                                                        gender="Female"
                                        if(re.match(r'\d{4} \d{4} \d{4}',text['DetectedText'])and text['Type']=='LINE'):
                                                print('AADhar number:' + text['DetectedText'])
                                                aadhar_no=text['DetectedText']
                                        if(re.search(r'[A-z][a-z]{1,} [A-Z][a-z]{1,}\s*[a-zA-Z]*',text['DetectedText']) and 'GOV' not in text['DetectedText'] and 'Gov' not in text['DetectedText'] and ":" not in text['DetectedText'] and text['Type']=='LINE'):
                                                print("Name:",text['DetectedText'])
                                                name=text['DetectedText']
                                        if(re.match('\d{10}',text['DetectedText'])):
                                                print("Mobile_no:",text['DetectedText'])
                                                mobile_no=text['DetectedText']

                return (name,gender,aadhar_no,mobile_no,DoB,address)
        # def getaddress(self,img2):




if __name__=='__main__':
        s=special.sc()
        print(s.getData('pp.jpeg'))
