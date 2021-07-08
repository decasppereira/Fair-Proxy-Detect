# Proxy Detection Scripts
These sets of scripts attempt to find **proxy** attributes of *protected* attributes within a dataset. 

## Binary Equivalence
This functionality is described by the ```simple_equivalence.py``` script and finds redundancy (equivalence) between *protected* and *non-protected* attributes of a dataset whose values are **binary**.

The way to run it is the following:
``` 
python simple_equivalence.py dataset_relative_path(.csv) num-total-attributes num-protected-attributes protected_feature_1 ... protected_feature_n
```
* ``` dataset_relative_path.csv``` is the relative path to from this folder to the dataset. It must be in ```.csv``` format.
* ``` num-total-attributes``` is the total number of attributes in the dataset, **including** the classification value.
* ```num-protected attributes``` is the number of *protected attributes* in the dataset
* Each *protected attribute* must then be disclosed with its column in the dataset, starting from 0.

This terminology will be used in the next scripts as well

## Categorical Equivalence
This functionality is described by the ```cat_equivalence.py``` script and finds redundancy (equivalence) between *protected* and *non-protected* attributes of a dataset whose values are **categorical**. 

The dataset must have been already treated to categorize all attribute values.

The way to run it is the following:
``` 
python cat_equivalence.py dataset_relative_path(.csv) num-total-attributes num-protected-attributes protected_feature_1 ... protected_feature_n
```

## Categorical Implication
This functionality is described by the ```cat_implication.py``` script and finds if any *non-protected* attribute **implies** any *protected* attribute of a dataset, whose values are **categorical**. 

The dataset must have been already treated to categorize all attribute values.

The way to run it is the following:
``` 
python cat_implication.py dataset_relative_path(.csv) num-total-attributes num-protected-attributes protected_feature_1 ... protected_feature_n
```

##Datasets and Running Instructions
### COMPAS
COMPAS comprises a list of criminals and their **recidivism classification**. It has a total of **12 attributes**, where **6** of them are *protected*:

##### Non-Protected Attributes:
* Number_of_Priors
* score_factor
* Age_Above_FourtyFive
* Age_Below_TwentyFive
* Misdemeanor

##### Protected Attributes:
* African_American
* Asian
* Hispanic
* Native_American
* Other
* Female

To run the aforemetioned scripts: 

```
python simple_equivalence.py ../../../bench/compas/compas.csv 12 6 4 5 6 7 8 9
python cat_equivalence.py ../../../bench/compas/compas.csv 12 6 4 5 6 7 8 9
python cat_implication.py ../../../bench/compas/compas.csv 12 6 4 5 6 7 8 9
```

### Adult
It has a total of **13 attributes**, where **3** of them are *protected*:
##### Non-Protected Attributes:
* Workclass
* Education
* Marital Status
* Occupation
* Relationship
* Capital Gain
* Capital Loss
* Hours per week
* Country

##### Protected Attributes:
* Age
* Race
* Sex

To run the aforemetioned scripts: 
```
python simple_equivalence.py ../../../bench/adult/adult_data.csv 13 3 0 6 7
python cat_equivalence.py ../../../bench/adult/adult_data.csv 13 3 0 6 7
python cat_implication.py ../../../bench/adult/adult_data.csv 13 3 0 6 7    
```


### German
It has a total of **22 attributes**, where **6** of them are *protected*:

##### Non-Protected Attributes:
* checking_status
* duration
* credit_history
* purpose
* credit_amount
* savings_status
* employment
* installment_commitment
* personal_status
* other_parties
* residence
* property_magnitude
* other_payment_plans
* housing
* existing_credits
* job
* num_dependents
* own_telephone

##### Protected Attributes:
* age
* age_cat
* foreign_worker

To run the aforemetioned scripts: 
```
python simple_equivalence.py ../../../bench/german-credit/german_data.csv 22 3 12 13 20
python cat_equivalence.py ../../../bench/german-credit/german_data.csv 22 3 12 13 20
python cat_implication.py ../../../bench/german-credit/german_data.csv 22 3 12 13 20    
```

### Titanic
It has a total of **8 attributes**, where **2** of them are *protected*:
#####Non-Protected Attributes:
* Pclass
* Name
* Siblings/Spouses Aboard
* Parents/Children Aboard
* Fare
#####Protected Attributes:
* Sex
* Age

To run the aforemetioned scripts: 
```
python simple_equivalence.py ../../../bench/titanic/titanic_data.csv 8 2 2 3
python cat_equivalence.py ../../../bench/titanic/titanic_data.csv 8 2 2 3
python cat_implication.py ../../../bench/titanic/titanic_data.csv 8 2 2 3 
```

