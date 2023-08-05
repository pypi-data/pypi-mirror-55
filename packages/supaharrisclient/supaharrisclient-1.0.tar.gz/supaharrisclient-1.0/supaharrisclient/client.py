import sys
import numpy
import logging
import requests
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
from platform import python_version

from . import __version__
from .utils import response_to_json
from .utils import print_progressbar


class SupaHarrisClient(object):
    def __init__(self, base_url="https://www.supaharris.com/api/v1/",
            loglevel=logging.DEBUG, set_all_data=True, verify=True):
        """ SupaHarris: a Python client implementation for the SupaHarris API

        Keyword arguments:
        base_url -- the base url of the API (could be localhost for development)
        loglevel -- verbosity of the output. Choose any one of
            logging.CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET """

        # Set up a logger to 'print' to stdout
        self.logger = logging.getLogger(__file__)
        self.logger.propagate = False
        self.logger.level = loglevel
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(loglevel)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.handlers = []
        self.logger.addHandler(handler)

        self.base_url = base_url

        # If we run locally (development), then we GET 443 /w self-signed certificate.
        # We tell the requests library not verify the ssl certificate, and we suppress
        # the InsecureRequestWarning.
        self.verify = verify
        if not self.verify:
            import urllib3
            urllib3.disable_warnings()

        url_params = "?format=json&length=1000"
        self.reference_list = "{0}catalogue/reference/{1}".format(
            self.base_url, url_params)
        self.astro_object_list = "{0}catalogue/astro_object/{1}".format(
            self.base_url, url_params)
        self.astro_object_classifcation_list = "{0}catalogue/astro_object_classifcation/{1}".format(
            self.base_url, url_params)
        self.parameter_list = "{0}catalogue/parameter/{1}".format(
            self.base_url, url_params)
        # Takes roughly 2 seconds to process a request /w 1000 Observation instances
        self.observation_list = "{0}catalogue/observation/{1}".format(
            self.base_url, url_params)

        self.headers = {
            "Accept": "application/json",
            "User-Agent": "SupaHarris for Python ({0}); Python ({1}).".format(
                __version__, str(python_version()))
        }

        if set_all_data: self.set_all_data()

    def set_reference_list(self):
        self.logger.info("Setting all Reference instances ...")
        self.references_json = self.get_list(self.reference_list, recursive=True)
        self.logger.info("  self.references_json is now available")

        self.references = numpy.array(
            [
                (r["id"], r["first_author"], getattr(r, "year", -1) if "year" in r.keys() else "",
                 r["title"], r["ads_url"])
                    for r in self.references_json
            ], dtype=[("id", "int"), ("first_author", "|U64"), ("year", "int"),
                      ("title", "|U128"), ("ads_url", "|U128")]
        )
        self.logger.info("  self.references is now available")
        self.logger.info("  len(self.references) = {0}".format(len(self.references)))
        self.logger.info("Done setting all Reference instances.\n")

    def print_references(self):
        self.logger.info("\nRetrieved {0} references\n".format(len(self.references)))

        self.logger.info("-"*79)
        self.logger.info("  {0:<5s}{1} ({2})".format("id", "first_author", "year"))
        self.logger.info("-"*79)
        for r in self.references_json:
            self.logger.info("  {0:<5d}{1} ({2})".format(
                r["id"], r["first_author"], r["year"] if "year" in r.keys() else ""))
        self.logger.info("-"*79)

    def set_astro_object_list(self):
        self.logger.info("Setting all AstroObject instances ...")
        self.astro_objects_json = self.get_list(self.astro_object_list, recursive=True)
        self.logger.info("  self.astro_objects_json is now available")

        self.astro_objects = numpy.array(
            [
                (ao["id"], ao["name"], ao["altname"] if ao["altname"] else "")
                    for ao in self.astro_objects_json
            ], dtype=[("id", "int"), ("name", "|U16"), ("altname", "|U16")]
        )
        self.logger.info("  self.astro_objects is now available")
        self.logger.info("  len(self.astro_objects) = {0}".format(len(self.astro_objects)))
        self.logger.info("Done setting all AstroObject instances.\n")

    def print_astro_objects(self):
        self.logger.info("\nRetrieved {0} astro_objects\n".format(len(self.astro_objects)))

        self.logger.info("-"*79)
        self.logger.info("  {0:<5s}{1:<15s}{2}".format("id", "name", "altname"))
        self.logger.info("-"*79)
        for o in self.astro_objects_json:
            self.logger.info("  {0:<5d}{1:<15s}{2}".format(
                o["id"], o["name"], o["altname"] if o["altname"] else ""))
        self.logger.info("-"*79)

    def set_astro_object_classification_list(self):
        self.logger.info("Setting all AstroObjectClassification instances ...")
        self.astro_object_classifications = self.get_list(
            self.astro_object_classifcation_list, recursive=True)
        self.logger.info("  self.astro_object_classifications is now available")
        self.logger.info("  len(self.astro_object_classifications) = {0}".format(len(self.astro_object_classifications)))
        self.logger.info("Done setting all AstroObjectClassification instances.\n")

    def print_astro_object_classifications(self):
        self.logger.info("\nRetrieved {0} astro_object_classifications\n".format(
            len(self.astro_object_classifications)))

        self.logger.info("-"*79)
        self.logger.info("  {0:<5s}{1:<15s}".format("id", "name"))
        self.logger.info("-"*79)
        for c in self.astro_object_classifications:
            self.logger.info("  {0:<5d}{1:<15s}".format(c["id"], c["name"] ))
        self.logger.info("-"*79)

    def set_parameter_list(self):
        self.logger.info("Setting all Parameter instances ...")
        self.parameters_json = self.get_list(self.parameter_list, recursive=True)
        self.logger.info("  self.parameters_json is now available")

        self.parameters = numpy.array(
            [
                (p["id"], p["name"]) for p in self.parameters_json
            ], dtype=[("id", "int"), ("name", "|U16")]
        )
        self.logger.info("  self.parameters is now available")
        self.logger.info("  len(self.parameters) = {0}".format(len(self.parameters)))
        self.logger.info("Done setting all Parameter instances.\n")

    def print_parameters(self):
        self.logger.info("\nRetrieved {0} parameters\n".format(len(self.parameters)))

        self.logger.info("-"*79)
        self.logger.info("  {0:<5s}{1:<15s}{2}".format("id", "name", "description"))
        self.logger.info("-"*79)
        for p in self.parameters_json:
            self.logger.info("  {0:<5d}{1:<15s}{2}".format(p["id"], p["name"], p["description"]))
        self.logger.info("-"*79)

    def set_observation_list(self, refresh=False):
        self.logger.info("Setting all Observation instances ...")

        if not hasattr(self, "parameters"):
            self.set_parameter_list()

        if not hasattr(self, "astro_objects"):
            self.set_astro_object_list()

        # First get 1 observation from the observation_list (~150 ms) to check the count.
        # No need to recursively GET observation_list if we already have all observations.
        for l in self.observation_list.split("&"):
            if "length=" in l: break
        one_observation = self.observation_list.replace(l, "length=1")
        response = requests.get(one_observation, headers=self.headers, verify=self.verify)
        if response.status_code != 200:
            self.logger.error("  Could not retrieve uri = '{0}'. Better stop.".format(uri))
            sys.exit(1)
        count = response_to_json(response)["count"]
        if hasattr(self, "observations") and len(self.observations) == count and not refresh:
            self.logger.info("  self.observations_json was already available, and (length) did not change")
        else:
            # There is a need to recursively GET all observations. Take ~2 seconds per page /w length=1000
            self.observations_json = self.get_list(self.observation_list, recursive=True)
            self.logger.info("  self.observations_json is now available")

        observations_array = numpy.array(
            [
                (o["astro_object"]["id"], o["astro_object"]["id"],
                 o["reference"]["id"], o["reference"]["bib_code"],
                 o["parameter"]["id"], o["parameter"]["id"],
                 o["value"], o["sigma_up"] if o["sigma_up"] else numpy.nan,
                 o["sigma_down"] if o["sigma_down"] else numpy.nan)
                    for o in self.observations_json
            ], dtype=[
                ("ao_id", "int"), ("ao_name", "|U16"),
                ("ref_id", "int"), ("ref_bib_code", "|U16"),
                ("p_id", "int"), ("p_name", "|U16"),
                ("value", "|U16"), ("sigma_up", "|U16"), ("sigma_down", "|U16")
            ]
        )
        dtype = [("name", "|U16" )] + [(p["name"], "|U16") for p in self.parameters]
        self.observations = numpy.empty(len(self.astro_objects), dtype=dtype)
        self.observations_ref = numpy.empty(len(self.astro_objects), dtype=dtype)
        # self.observations[:] = numpy.nan
        for i, (ao_id, ao_name) in enumerate(zip(self.astro_objects["id"], self.astro_objects["name"])):
            self.observations[i]["name"] = ao_name
            for j, (p_id, p_name) in enumerate(zip(self.parameters["id"], self.parameters["name"])):
                # if i < 2: print("{:>4d}{:>4d}{:>16s}{:>4d}{:>4d}{:>16s} ".format(
                #     i, ao_id, ao_name, j, p_id, p_name), end="")

                has_obs, = numpy.where(
                    (observations_array["p_id"] == p_id)
                    & (observations_array["ao_id"] == ao_id)
                )
                if len(has_obs) >= 1:
                    # TODO: at a later point in time we should handle multiple
                    # observations of the same parameter / astro_object combination...
                    self.observations[i][p_name] = observations_array["value"][has_obs][0]
                    self.observations_ref[i][p_name] = observations_array["ref_bib_code"][has_obs][0]
                # if i < 2: print(has_obs, observations_array["value"][has_obs], self.observations[i][p_name])
            # if i < 2: print("")
        self.logger.info("  self.observations is now available")
        self.logger.info("  len(self.observations) = {0}".format(len(self.observations)))
        self.logger.info("Done setting all Observation instances.\n")

    def set_all_data(self):
        self.set_parameter_list()
        self.set_reference_list()
        self.set_astro_object_list()
        self.set_astro_object_classification_list()
        self.set_observation_list()

    def get_list(self, uri, recursive=False, total_count=0):
        """ Send a GET request to the SupaHarris API endpoint uri. The Django
        REST response contains 'count' (int), 'next' (string), 'previous' (string),
        'results' (list). The response is paginated so we recursively GET the
        'next' uri until 'next' is 'null' (JSON) / None (Python). At that point
        len(results) should equal the value of count. """

        self.logger.debug("GET {0}".format(uri))

        response = requests.get(uri, headers=self.headers, verify=self.verify)
        if response.status_code != 200:
            self.logger.error("  Could not retrieve uri = '{0}'. Better stop.".format(uri))
            sys.exit(1)

        results = []

        data = response_to_json(response)
        count = data["count"]
        next = data["next"]
        results += data["results"]
        total_count += len(results)
        self.logger.debug("  retrieved {0}/{1} instances".format(total_count, count))
        self.logger.debug("  next = {0}{1}".format(next, "\n" if not next else ""))

        if next and recursive:
            results += self.get_list(next, recursive=True, total_count=total_count)

        return results

    def __str__(self):
        return "SupaHarrisClient for '{0}'".format(self.base_url)
