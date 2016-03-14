from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
import datetime
import json
from ticketing.factories import ClientFactory, ProductFactory, FeatureRequestFactory, UserFactory
from ticketing.models import Client, Product, FeatureRequest
from ticketing.forms import FeatureRequestForm


class TestLogin(TestCase):

    def setUp(self):
        self.user = UserFactory(username="test")

    def test_authentication_control(self):
        request = self.client.get(reverse('login'))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'login.html')

        self.client.login(username="test", password="test")
        request = self.client.get(reverse('login'))
        self.assertEqual(request.status_code, 302)
        self.assertEqual(request.url, reverse('index'))


class TestHomePage(TestCase):

    def setUp(self):
        self.user = UserFactory(username="test")

    def test_homepage_authentication_control(self):
        request = self.client.get(reverse('index'), follow=True)
        self.assertRedirects(request, '/login/?next=/')

        self.client.login(username="test", password="test")
        request = self.client.get(reverse('index'))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'index.html')

    def test_get_action(self):
        self.featurerequest = FeatureRequestFactory.create_batch(4)

        self.client.login(username="test", password="test")

        request = self.client.get(reverse('index'))
        self.assertEqual(len(request.context['clients']), 4)

        self.assertTemplateUsed(request, 'index.html')

    def test_post_action_with_no_data(self):

        self.client.login(username="test", password="test")

        response = self.client.post(reverse('index'))
        self.assertFormError(response, "form", "title",
                             "This field is required.")
        self.assertFormError(
            response,
            "form",
            "desc",
            "Please enter a description of the feature request.")
        self.assertFormError(
            response,
            "form",
            "targetdate",
            "This field is required.")
        self.assertFormError(
            response,
            "form",
            "client",
            "This field is required.")
        self.assertFormError(
            response,
            "form",
            "productarea",
            "This field is required.")

    def test_post_action(self):
        self.featurerequest = FeatureRequestFactory.create_batch(4)

        self.client.login(username="test", password="test")

        response = self.client.post(
            reverse('index'),
            data={
                'title': 'New Feature Test',
                'desc': 'This is a test desc',
                'targetdate': '03/24/2016',
                'url': 'http://www.example.com',
                'client': self.featurerequest[0].client.pk,
                'productarea': self.featurerequest[0].productarea.pk
            }
        )

        self.assertIsNotNone(
            FeatureRequest.objects.get(
                title="New Feature Test"))

    def test_post_action_with_no_previous_feature(self):
        self.apclient = ClientFactory()
        self.approduct = ProductFactory()

        self.client.login(username="test", password="test")

        response = self.client.post(
            reverse('index'),
            data={
                'title': 'New Feature Test',
                'desc': 'This is a test desc',
                'targetdate': '03/24/2016',
                'url': 'http://www.example.com',
                'client': self.apclient.pk,
                'productarea': self.approduct.pk
            }
        )

        self.assertIsNotNone(
            FeatureRequest.objects.get(
                title="New Feature Test"))


class TestFeaturePage(TestCase):

    def setUp(self):
        self.user = UserFactory(username="test")

    def test_get_action(self):

        self.appclient = ClientFactory.create_batch(4)

        self.client.login(username="test", password="test")

        request = self.client.get(reverse('feature-list'))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'feature.html')

    def test_post_action(self):

        self.featurerequest = FeatureRequestFactory.create_batch(4)

        self.client.login(username="test", password="test")

        request = self.client.post(
            reverse('feature-list'), {'client': self.featurerequest[0].client.pk})
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'feature.html')
        content = request.content.decode()
        self.assertIn(str(self.featurerequest[0].title), content)
        self.assertIn(str(self.featurerequest[0].productarea), content)
        self.assertIn(str(datetime.datetime.strptime(self.featurerequest[
                      0].targetdate, '%Y-%m-%d').strftime('%B %d, %Y')), content)
        self.assertIn(self.featurerequest[0].url, content)
        self.assertIn(str(self.featurerequest[0].client), content)

    def test_post_action_with_invalid_form(self):

        self.featurerequest = FeatureRequestFactory.create_batch(4)

        self.client.login(username="test", password="test")

        request = self.client.post(reverse('feature-list'), {'client': 100})
        self.assertIn(
            'No Data To Display. Please Choose a Client.',
            request.content.decode())


class TestFeatureDetailsPage(TestCase):

    def setUp(self):
        self.user = UserFactory(username="test")

    def test_get_action(self):

        self.featurerequest = FeatureRequestFactory.create_batch(4)

        self.client.login(username="test", password="test")

        request = self.client.get(
            reverse('feature-list') + str(self.featurerequest[0].pk) + '/')
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'feature-details.html')
        content = request.content.decode()
        self.assertIn(str(self.featurerequest[0].title), content)
        self.assertIn(str(self.featurerequest[0].productarea), content)
        self.assertIn(str(datetime.datetime.strptime(self.featurerequest[
                      0].targetdate, '%Y-%m-%d').strftime('%B %d, %Y')), content)
        self.assertIn(self.featurerequest[0].url, content)
        self.assertIn(str(self.featurerequest[0].client), content)


# class TestUpdatePriority(TestCase):

        # def setUp(self):
        # self.user = UserFactory(username="test")

        # def test_post_action(self):

        # self.featurerequest = FeatureRequestFactory.create_batch(4)

        # self.client.login(username="test", password="test")

        # request = self.client.post(reverse('feature-priority-update'), content_type='application/json', data={"pk":self.featurerequest[0].pk,"priority":"100"})
        # print(reverse('feature-priority-update'))
        # kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}
        # response = self.client.post(
        # reverse('feature-priority-update'),
        # data={
        # "pk": str(self.featurerequest[0].pk),
        # "priority": "100"
        # },
        # )
        # self.assertEqual(FeatureRequest.objects.get(pk=self.featurerequest[0].pk).priority, 100)
        # print(response.content)


class TestDataPresentation(TestCase):

    def setUp(self):
        self.user = UserFactory(username="test")
        self.featurerequest = FeatureRequestFactory()

    def test_post_action(self):

        self.client.login(username="test", password="test")

        request = self.client.get(reverse('data-presentation'))
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'data-presentation.html')

        self.assertEqual(request.context['count'], 1)
        self.assertEqual(len(request.context['clients']), 1)
        self.assertEqual(request.context['total_features'], 1)
        self.assertEqual(
            request.context['client_feature_percent'], {
                self.featurerequest.client.name: 100})
        self.assertEqual(request.context['product_feature_total'], {
                         self.featurerequest.productarea.name: 1})
        self.assertEqual(
            request.context['target_date_total'], {
                '2016-3-24': 1})

    def test_if_condition_in_post_action(self):

        self.client.login(username="test", password="test")

        request = self.client.post(reverse('data-presentation'))
        self.assertEqual(request.status_code, 302)
        self.assertEqual(request.url, reverse('index'))
