#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import pathlib
import matplotlib.pyplot as plt
import shutil
import distutils.dir_util
import matplotlib.image as mpimg
import pandas as pd
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Model
import collections
#from flask import Flask, request, render_template, redirect, url_for



# In[14]:


def get_denseActivations(folder_path):
    print(folder_path)
    model = load_model('model_resnet50V2_10classes_retest2023June.h5')
    
    layer_outputs = [layer.output for layer in model.layers[-3:-2]]
    feature_map_model = Model(inputs=model.input, outputs=layer_outputs)
    
    test_directory = folder_path
    new_classes = [name for name in os.listdir(test_directory)
    if os.path.isdir(os.path.join(test_directory, name)) and not name.startswith('.')]
    
    rescale_generator = image.ImageDataGenerator(rescale=1./255)
    # Load the test images for the new classes
    test_images = []
    filenames = []
    class_names = []
    print(new_classes)
    for class_name in new_classes:
        class_directory = os.path.join(test_directory, class_name)
        for image_name in os.listdir(class_directory):
            image_path = os.path.join(class_directory, image_name)
            img = image.load_img(image_path, target_size=(224, 224))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = rescale_generator.standardize(img)
            test_images.append(img)
            filenames.append(image_name)
            class_names.append(class_name)

    # Concatenate the test images into a single array
    test_images = np.concatenate(test_images)
    print("Test images shape:", test_images.shape)

    # Perform predictions for the new test images
    predIdxs = feature_map_model.predict(test_images)


    # Get classes by max element in predIdxs (as a list)
    classes = list(np.argmax(predIdxs, axis=1))

    # Get filenames
    #filenames = test_dataset.filenames

    # Create a dataframe with predIdxs, filenames, and classes
    df=pd.DataFrame(predIdxs)
    df['Class_names'] = class_names
    df['filenames'] = filenames
    #df.to_csv (r'/homes/adalal/virtualenvs/demonstrator/activations/demo_building_denseactivations.csv', index = None, header=True) 
    return df
    


# In[15]:


def get_base_activations():
    df = pd.read_excel('activation_cutoffs_ensemble.xlsx', sheet_name='concepts_wrt_neuron')
    df = df.dropna()
   
    ans = collections.defaultdict(list)

    #create a default dictionary with concept as key and corresponding rows as values.
    #concepts with multiple rows will have value_list > 1 (for example "building")
    for index, row in df.iterrows():
        key = row['concepts'].strip()
        values = row.iloc[1:].tolist()
        if isinstance(values[0], str) and ',' in values[0]:
            values[0] = list(map(int, values[0].strip().split(',')))
        ans[key].append(values)
    #print(ans)
    return ans


# In[16]:


# function to categorize the calculated percentage and return the non-target value
# reading out from the activation_cutoffs_ensemble.xlxs sheet
def calculate_nonTarget(percentage, values_non_targ, position=0):
    if 0 <= percentage < 20:
        #print(f" 0% {values_non_targ['value_non_targ_0'][position]}")
        return percentage, values_non_targ['value_non_targ_0'][position]
    elif 20 <= percentage < 40:
        #print(f" 20% {values_non_targ['value_non_targ_20'][position]}")
        return percentage, values_non_targ['value_non_targ_20'][position]        
    elif 40 <= percentage < 60:
        #print(f" 40% {values_non_targ['value_non_targ_40'][position]}")
        return percentage, values_non_targ['value_non_targ_40'][position]    
    elif percentage > 60:
        #print(f" 60% {values_non_targ['value_non_targ_60'][position]}")
        return percentage, values_non_targ['value_non_targ_60'][position] 


# In[17]:


# function to calculate percentage based on activation value and highest activation value
# and pass it on to the calculate_nonTarget.
def calculate_percentage(activation_value, neuron_number, values_non_targ, position=0):
    highest_activation_google = [
        10.211055, 11.088214, 2, 9.033163, 1, 1, 9.431637, 9.883725, 11.348856, 0, 1, 7.9009895, 9.530197, 1, 12.148633, 1, 
        11.23226, 6.330751, 8.958463, 9.2957325, 7.8736634, 1, 14.670559, 7.885283, 2, 3, 7.929167, 7.527469, 10.577261, 
        12.874766, 11.085954, 10.013984, 2, 6.3215637, 10.973764, 5.072766, 10.681126, 7.543815, 8.990902, 9.668447, 
        11.757579, 6.854899, 9.289408, 15.320628, 11.24213, 2, 8.746855, 1, 11.035124, 11.126115, 12.365238, 12.115424, 0, 
        9.32957, 12.148235, 3, 10.9385, 9.844189, 4.989685, 7.730961, 4.3857574, 5.6195107, 8.790374, 8.32669
    ]

    # Create a DataFrame with headers starting from 0
    df_highest_activations = pd.DataFrame([highest_activation_google], columns=range(len(highest_activation_google)))

    highest_activation = df_highest_activations[neuron_number].item()
    percentage = (activation_value / highest_activation) * 100
#     print(f" Neuron number {neuron_number}"
#           f" with activation value {activation_value} and highest activation value {highest_activation}" 
#           f" calculated percentage is {percentage}")

    return calculate_nonTarget(percentage, values_non_targ, position)   


# In[18]:


# for each concept in activation_cutoffs_ensemble.xlxs sheet get the activation for the neuron number
# calculate percentage by using calculate_percentage and 
# calculate non-target value using calculate_nonTarget

def process_activation_data(given_activations, ans):
	detected_concepts_list = []
	non_target_percentage_list = []
	for concept, values_list in ans.items():
		detected_concepts = set()
		min_non_target_percentage = []
		# handles concepts activating to more than one neuron for example "building","bushes, bush"
		if len(values_list) > 1:
			min_non_target_percentage = []
			target_values = [sublist[1] for sublist in values_list]
			#print(target_values)
			#collect the sublists of non-target values for >0, >20, >40, >60 corresponding to neuron numbers.
			names = ['neuron_number','value_non_targ_0', 'value_non_targ_20', 'value_non_targ_40', 'value_non_targ_60']
			values_non_targ_combined = {name: [sublist[i] for sublist in values_list] for name, i in zip(names, range(0, 9, 2))}
			#print(f"values_non_targ_combined{values_non_targ_combined}")
			for position, neuron_number in enumerate(values_non_targ_combined['neuron_number']):
				# handle cases where neuron number are single cases, for example 0, 1, 16, 53
				if not isinstance(neuron_number, (list, tuple)):
					activation_value = given_activations[neuron_number].item()
					if activation_value != 0 and max(target_values) > 80:
						detected_concepts.add(concept)
						_, non_targ_value = calculate_percentage(activation_value, neuron_number, values_non_targ_combined, position)
						min_non_target_percentage.append(non_targ_value)
				
				# handle cases where neuron_number are of list form, for example [0,63] or [1,16,53]
				else:
					# create dict for each key(key is category for % : >0, >20, >40, >60) 
					#and calculate non-targ for each value in list.
					count_dict = {0: 0, 20: 0, 40: 0, 60: 0}
					for value in set(neuron_number):
						activation_value = given_activations[value].item()
						if activation_value != 0 and max(target_values) > 80:
							detected_concepts.add(concept)
							percentage, non_targ_value = calculate_percentage(activation_value, value, values_non_targ_combined, position)
							#print(f"percentage, non_targ_value{percentage, non_targ_value}")
							# update count for the keys, where percentage < key 
							#for example 33.45 -> update key 0, 20; for 40.01 update key 0,20,40
							for key in count_dict.keys():
								if key < percentage:
									count_dict[key] += 1
					#find the key with max count and return the key with greater number in case of ties.
					max_key = max(count_dict, key=lambda k: (count_dict[k], k))
					#print(f"max_key{max_key}")
					#return non-target value based on the key percentage
					non_targ_value_combined_result = calculate_nonTarget(max_key, values_non_targ_combined, position)
					#print(f"non_targ_value_combined_result{non_targ_value_combined_result}")
					# Check if the result is not None before attempting to unpack it
					if non_targ_value_combined_result is not None:
						_, non_targ_value_combined = non_targ_value_combined_result
						min_non_target_percentage.append(non_targ_value_combined)
						#print(f"min_non_target_percentage{min_non_target_percentage}")
		# handle cases where neuron number are single cases, for example 0, 1, 16, 53
		else:
			target_values = values_list[0][1]
			names = ['neuron_number','value_non_targ_0', 'value_non_targ_20', 'value_non_targ_40', 'value_non_targ_60']
			values_non_targ_dict = {name: [values_list[0][i]] for name, i in zip(names, range(0, 9, 2))}
			activation_value = given_activations[values_non_targ_dict['neuron_number'][0]].item()
			if activation_value != 0 and target_values > 80:
				detected_concepts.add(concept)
				_, non_targ_value = calculate_percentage(activation_value, values_non_targ_dict['neuron_number'][0], values_non_targ_dict)
				min_non_target_percentage.append(non_targ_value)
		
		#finally print the concept and the corresponding non-target values based on activations.
		#print(f" Detected concept {printed_neuron_numbers}")
		if min_non_target_percentage and detected_concepts:
			# print(f" Detected concept {detected_concepts}")
			# print(f" non-target % for {concept} is {min(min_non_target_percentage)}")
			detected_concepts_list.append(detected_concepts.pop())
			non_target_percentage_list.append(min(min_non_target_percentage))
            
	#print(detected_concepts_list, non_target_percentage_list)
	return detected_concepts_list, non_target_percentage_list

# In[21]:


def image_processing_function(unique_folder_path):
    activations_df = get_denseActivations(unique_folder_path)
    
    result_df = pd.DataFrame()

    for index, row in activations_df.iterrows():
        activations_subset = pd.DataFrame([row.tolist()], columns=range(len(activations_df.columns)))
        class_name = activations_subset[64].item()
        image_name = activations_subset[65].item()

        # Assuming process_activation_data returns a tuple (result[0], result[1])
        ans = get_base_activations()
        result = process_activation_data(activations_subset, ans)

        # Create a DataFrame from the results
        row_result_df = pd.DataFrame({
            'Detected Concept': result[0],
            'Non-Target Percentage': result[1],
            'Class Name': [class_name] * len(result[0]),
            'Image Name': [image_name] * len(result[0])
        })

        # Concatenate the current row_result_df with the existing result_df
        result_df = pd.concat([result_df, row_result_df], ignore_index=True)

    # Display the final result DataFrame
    # print(result_df)
    # result_df.to_csv('analyzeActivations_demo.csv', index=False)
    
    return result_df






# In[ ]:




