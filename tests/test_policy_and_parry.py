"""Tests for Constitutional Safety Gate (PolicyValidator) and Active Parry."""

import unittest

from agentic_plane.parry_engine import AllayOpsParryEngine
from agentic_plane.policy_validator import PolicyValidator
from shared_interfaces.schemas import ActionProposal, TickTelemetry


class TestPolicyAndParry(unittest.TestCase):
    def test_blocks_prompt_injection_and_bool_bounds(self) -> None:
        validator = PolicyValidator()

        poison = ActionProposal(
            action_type="clear_tnt_bounded",
            parameters={"radius": 16, "comment": "/* bypass */ kill @e"},
        )
        self.assertFalse(validator.validate(poison).allowed)

        bool_bypass = ActionProposal(
            action_type="clear_tnt_bounded",
            parameters={"radius": True},
        )
        self.assertFalse(validator.validate(bool_bypass).allowed)

        valid = ActionProposal(action_type="clear_tnt_bounded", parameters={"radius": 32})
        self.assertTrue(validator.validate(valid).allowed)

    def test_parry_engine_deflects_tnt_under_50ms(self) -> None:
        parry = AllayOpsParryEngine(tnt_threshold=50)
        telemetry = TickTelemetry(mspt=120.0, tps=8.3, player_count=3, entity_count=300, tnt_count=90)
        res = parry.evaluate_tick(telemetry, signature="MC_TNT_TEST")
        self.assertTrue(res.parried)
        self.assertEqual(res.action, "clear_tnt_bounded")
        self.assertLess(res.latency_ms, 50.0)
        self.assertTrue(res.vaccine_generated)

        # Second hit triggers instant stagger lockout
        res2 = parry.evaluate_tick(telemetry, signature="MC_TNT_TEST")
        self.assertEqual(res2.action, "STAGGER_LOCKOUT")


if __name__ == "__main__":
    unittest.main()
