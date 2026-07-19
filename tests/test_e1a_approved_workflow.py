from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from adaptive_learning.application_service import ApplicationService


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACK_PATH = REPOSITORY_ROOT / "packs" / "amateur-extra-e1a"
GOLDEN_PATH = REPOSITORY_ROOT / "tests" / "fixtures" / "amateur-extra-e1a-approved.json"
APPROVED_DIGEST = "08bf23dab11ea27ed945f94bd6dbcf8892e156726a7596144df4d8b4610cb73e"


class ApprovedE1AWorkflowTests(unittest.TestCase):
    def test_approved_pack_offline_install_study_restart_and_challenge(self) -> None:
        golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            data_path = Path(temporary) / "user-data"
            with patch("socket.create_connection") as connect, patch("urllib.request.urlopen") as urlopen:
                service = ApplicationService(data_path)
                health = service.system_health()
                self.assertEqual(health["schema_version"], "1")
                self.assertEqual(health["pack_format_versions"], ["0.1", "0.2"])

                validation = service.pack_validate(PACK_PATH)
                self.assertEqual(validation["pack_digest"], APPROVED_DIGEST)
                self.assertEqual(validation["official_question_count"], 11)
                self.assertEqual(validation["question_origins"], {"official_pool": 11, "generated": 0})
                self.assertEqual(validation["approval"]["reviewed_by"], "Anthony McClure")

                installation = service.pack_install(PACK_PATH)
                self.assertTrue(installation["installed"])
                self.assertEqual(installation["pack_digest"], APPROVED_DIGEST)

                learner = service.learner_initialize("E1A acceptance learner")
                started = service.study_start(learner["learner_id"], "us-amateur-extra-e1a", "0.2.0")
                self.assertEqual(
                    [lesson["lesson_id"] for lesson in started["lessons"]],
                    ["lesson-band-edges", "lesson-special-operations"],
                )

                presented = service.study_next(started["session_id"])
                question = presented["question"]
                self.assertEqual(question["official_question_id"], "E1A01")
                self.assertEqual(question["prompt"], golden["questions"][0]["prompt"])
                self.assertEqual(question["options"], golden["questions"][0]["options"])
                self.assertNotIn("correct_option_ids", question)
                self.assertNotIn("explanation", question)
                self.assertNotIn("explanation_citations", question)

                feedback = service.study_submit(
                    started["session_id"], presented["presentation_id"], ["D"], 4
                )
                self.assertTrue(feedback["is_correct"])
                self.assertEqual(feedback["confidence"], 4)
                self.assertEqual(feedback["provenance"]["official_question_id"], "E1A01")
                self.assertEqual(
                    feedback["provenance"]["explanation_citations"][0]["source"]["publisher"],
                    "Federal Communications Commission",
                )

                restarted = ApplicationService(data_path)
                status = restarted.study_status(learner["learner_id"])
                self.assertEqual(status["active_session"]["session_id"], started["session_id"])
                resumed = restarted.study_start(
                    learner["learner_id"], "us-amateur-extra-e1a", "0.2.0"
                )
                self.assertTrue(resumed["resumed"])
                retry = restarted.study_submit(
                    started["session_id"], presented["presentation_id"], ["D"], 4
                )
                self.assertEqual(retry["attempt_id"], feedback["attempt_id"])

                second = restarted.study_next(started["session_id"])
                self.assertEqual(second["question"]["official_question_id"], "E1A02")
                challenge = restarted.question_challenge(
                    started["session_id"], second["presentation_id"], "Acceptance quarantine check"
                )
                self.assertTrue(challenge["quarantined"])
                self.assertEqual(
                    restarted.study_status(learner["learner_id"])["active_session"]["challenged_count"],
                    1,
                )

                connect.assert_not_called()
                urlopen.assert_not_called()


if __name__ == "__main__":
    unittest.main()
