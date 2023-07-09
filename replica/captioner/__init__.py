from transformers import pipeline

captioner = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")
captioner("/Users/valentinafeve/Downloads/attachments/Colin Sippl (+4917682347617)/image-92.jpg")
