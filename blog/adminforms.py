from django import forms


class PostAdminForm(forms.ModelForm):
    # 把摘要改为Textarea组件
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)