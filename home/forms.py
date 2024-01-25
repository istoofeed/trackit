from django import forms
from django.core.validators import validate_email

from adviser.models import PendingAdvisory, UserTask
from users.models import Group, User


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "name",
            "username",
            "email",
            "course",
            "user_role",
            "profile_picture",
        ]

        widgets = {"profile_picture": forms.FileInput()}

    def clean_name(self):
        name = self.cleaned_data["name"]

        if not name:
            raise forms.ValidationError("Please enter a name")

        return name

    def clean_username(self):
        username = self.cleaned_data["username"]

        if not username:
            raise forms.ValidationError("Please enter a username")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not email:
            raise forms.ValidationError("Please enter an email address")
        if validate_email(email) == False:
            raise forms.ValidationError("Please enter a valid email address")

        return email

    def clean_course(self):
        course = self.cleaned_data["course"]

        if not course:
            raise forms.ValidationError("Please enter a course")

        return course

    def clean_user_role(self):
        user_role = self.cleaned_data["user_role"]

        if not user_role:
            raise forms.ValidationError("Please enter a user_role")

        return user_role

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret


class FileUploadForm(forms.ModelForm):
    file = forms.FileField(
        required=False,
        label="Upload File:",
        widget=forms.FileInput(attrs={"accept": ".pdf, .docx, .zip"}),
    )

    class Meta:
        model = UserTask
        fields = ["file"]

        labels = {"file": "Upload File:"}

    def clean_file(self):
        file = self.cleaned_data["file"]

        if not file:
            raise forms.ValidationError("Please upload a file")

        allowed_extensions = ["docx", "pdf", "zip"]
        extension = file.name.split(".")[-1].lower()
        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Invalid file format. Please upload a docx, pdf, or zip file."
            )

        return file

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret


class PendingAdvisoryForm(forms.ModelForm):
    file = forms.FileField(
        required=False,
        label="Insert a file to review:",
        widget=forms.FileInput(attrs={"accept": ".pdf, .docx, .zip"}),
    )

    class Meta:
        model = PendingAdvisory
        fields = ["proposed_title", "file"]

    def clean_proposed_title(self):
        proposed_title = self.cleaned_data["proposed_title"]

        if not proposed_title:
            raise forms.ValidationError("Please a your proposed title")

        return proposed_title

    def clean_file(self):
        file = self.cleaned_data["file"]

        if not file:
            raise forms.ValidationError("Please upload a file")

        allowed_extensions = ["docx", "pdf", "zip"]
        extension = file.name.split(".")[-1].lower()
        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Invalid file format. Please upload a docx, pdf, or zip file."
            )

        return file

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            "name",
        ]

    def clean_name(self):
        name = self.cleaned_data["name"]

        if not name:
            raise forms.ValidationError("Please enter a title")

        return name

    def is_valid(self):
        ret = forms.Form.is_valid(self)

        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret
