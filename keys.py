# cognitive services

'''
these keys are no longer working, please change them accordingly to those found in your azure account
'''


subscription_key = "replace_with_your_own_key"
region = "replace_with_your_own_region"
prediction_endpoint = "https://cwb-cognitiveservices.cognitiveservices.azure.com/customvision/v3.0/Prediction/85ae3371-e249-486b-801f-c5aa9fba4553/classify/iterations/Iteration1/image"


# custom vision
project_id = "85ae3371-e249-486b-801f-c5aa9fba4553"
model_name = "cwb-SignLanguage"
iterationId	= "92eeec03-9abe-41c6-823c-63a3efd0eb02"
endpoint = "https://cwb-cognitiveservices.cognitiveservices.azure.com/"


# dictionary

'''
the dictionaries are hardcoded with the tag_ids from my custom vision training which is
not necessary to include them. i believe there are more simple ways to retrieve the images
by reading the files locally but the project requirements included the training of custom 
hand sign language images so feel free to remove them.
'''

tags = {
            'A': "77fb2660-0cfc-4d9d-9661-07485b1b2cd4", 
            'B': "da6dae58-a782-481e-8514-0d4ce63c429f", 
            'C': "752c1844-df6b-4c31-abb6-491690926ab2", 
            'D': "a34124bd-80d3-423a-a63a-baa1d81381a5", 
            'E': "de5944b1-fb03-4214-830c-0df2b919e94e", 
            'F': "02ccf2a7-5bb5-4d11-936c-3c812304f45f", 
            'G': "fd62aad9-95a1-44b1-842d-050df30bcb9e", 
            'H': "a3d7d606-7380-4151-a2b9-5fe9866349b5", 
            'I': "17cbabba-4440-4a30-918e-6a296f110396", 
            'J': "8a76aded-bdcd-4668-823f-e4eae9ba27b2", 
            'K': "c489f975-da09-4f25-9e8c-a4e66b8e453f", 
            'L': "3d290cab-b11e-4bdd-996a-971815729051", 
            'M': "b9001182-4a36-4c70-9740-65c34a22dbd7", 
            'N': "5c90f3ea-32b8-4529-bcc9-c8caf40dece8", 
            'O': "9c59a885-7d2a-4404-8a1f-cb88005f6f22", 
            'P': "49ef049c-da0f-4e27-96c6-5705c24298b4", 
            'Q': 'db685bd1-70e2-4879-ab71-a8824da0fb69', 
            'R': "b30ea888-4c9c-48ba-8d9e-08f47a6ac39d", 
            'S': "ab6c33de-a18a-42cf-955d-e1da2f1e5a56", 
            'T': "2e670647-9f18-429c-a393-c82553e4f876", 
            'U': "fdcb52bd-4841-4255-97d6-e7206b2e6140", 
            'V': "956e4449-b3fb-4829-a63e-b1ff3f725686", 
            'W': "a2c8b699-4380-46d9-a8b1-883718a8bf3a", 
            'X': "f1fadde7-5c6a-4fac-a7b3-580f5c0b0ead", 
            'Y': "90f8bc59-1015-472c-a45e-ee1da8e12f8d", 
            'Z': "427c921c-d1ad-4373-b572-7ebb4292b840", 
            ' ': "030ea132-dfd4-41e6-a1b5-d8318db501c1", 
            'Del': "bc10952d-2c94-4df1-a331-98a0dc4de0d2" 

    }

image_ref = {
            'A': 'A',
            'B': 'B',
            'C': 'C',
            'D': 'D',
            'E': "E", 
            'F': "F", 
            'G': "G", 
            'H': "H", 
            'I': "I", 
            'J': "J", 
            'K': "K", 
            'L': "L", 
            'M': "M", 
            'N': "N", 
            'O': "O", 
            'P': "P", 
            'Q': 'Q', 
            'R': "R", 
            'S': "S", 
            'T': "T", 
            'U': "U", 
            'V': "V", 
            'W': "W", 
            'X': "X", 
            'Y': "Y", 
            'Z': "Z", 
            ' ': "Space", 
    
}

def add_dict():

    special_characters = [ '@', '[', '_', '!', '#', '$', '%', '^', '&',
                            '*', '(', ')', '<', '>', '?', '/', '}', '.',
                            '{', '~', ':', ']']

    for i in special_characters:
        tags[i] = "4d92c161-3daa-4533-8010-fb4bdb232a67"
        image_ref[i] = "Nothing"


