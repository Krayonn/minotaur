from django.db import models
import json
import decimal

class Compound(models.Model):
    # Make primary key
    compound_id = models.IntegerField(primary_key=True)
    smiles = models.CharField(max_length=100)
    molecular_weight = models.DecimalField(max_digits=10, decimal_places=5)
    a_log_p = models.DecimalField(max_digits=10, decimal_places=3)
    molecular_formula = models.CharField(max_length=50)
    num_rings = models.IntegerField()
    image = models.CharField(max_length=50)

    def __str__(self):
        dict = {'compound_id':self.compound_id,
                'smiles':self.smiles,
                'molecular_weight':self.molecular_weight,
                'a_log_p':self.a_log_p,
                'molecular_formula':self.molecular_formula,
                'num_rings':self.num_rings,
                'image':self.image
                }

        return json.dumps(dict)

    @classmethod
    def create(self, **kwargs):
        compound = self.objects.create(
            compound=kwargs['compound'],
            smiles=kwargs['smiles'],
            molecular_weight=decimal.Decimal(kwargs['molecular_weight']),
            a_log_p=decimal.Decimal(kwargs['ALogP']),
            molecular_formula=kwargs['molecular_formula'],
            num_rings=kwargs['num_rings'],
            image=kwargs['image']
        )
        for assay_result in kwargs['assay_results']:
            assay, created = Assay.objects.get_or_create(
                compound_id=compound_id,
                result_id=assay_result['result_id'],
                target=assay_result['target'],
                result=assay_result['result'],
                operator=assay_result['operator'],
                value=assay_result['value'],
                unit=assay_result['unit']
            )
        print('Added compound with related assays..')
        return compound


class Assay(models.Model):
    # Create field to represent compound it comes from - foreignKey used for Many to on relationships
    # on_delete=models.CASCADE means if compound is deleted so are its results
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE, related_name='assay_results')
    # Make primary key
    result_id = models.IntegerField(primary_key=True)
    target =  models.CharField(max_length=50)
    result = models.CharField(max_length=10)
    operator = models.CharField(max_length=3)
    value = models.FloatField()
    unit = models.CharField(max_length=10)

    def __str__(self):
        return self.result_id
