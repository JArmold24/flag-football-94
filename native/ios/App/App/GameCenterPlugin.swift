import Foundation
import UIKit
import Capacitor
import GameKit

/// A small local Capacitor plugin for Game Center: sign the player in, post the Superstar legacy score to the
/// Hall of Fame leaderboard, unlock career achievements, and open the Game Center leaderboard / achievement views.
/// JavaScript calls it as plugin "GameCenter" (see the native layer in the game's src/native.js).
@objc(GameCenterPlugin)
public class GameCenterPlugin: CAPPlugin, CAPBridgedPlugin, GKGameCenterControllerDelegate {
    public let identifier = "GameCenterPlugin"
    public let jsName = "GameCenter"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "signIn", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "status", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "submitScore", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "reportAchievement", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "showLeaderboard", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "showAchievements", returnType: CAPPluginReturnPromise),
    ]

    private var handlerInstalled = false

    /// Installs Game Center's authentication handler once. Game Center calls it again whenever the
    /// sign-in state changes; if it hands back a sign-in sheet, it is shown over the game.
    @objc func signIn(_ call: CAPPluginCall) {
        DispatchQueue.main.async { [weak self] in
            guard let self = self else { return }
            let player = GKLocalPlayer.local
            if player.isAuthenticated {
                call.resolve(["authenticated": true, "name": player.displayName])
                return
            }
            if self.handlerInstalled {
                call.resolve(["authenticated": false])
                return
            }
            self.handlerInstalled = true
            var answered = false
            player.authenticateHandler = { [weak self] viewController, error in
                if let viewController = viewController {
                    DispatchQueue.main.async { self?.bridge?.viewController?.present(viewController, animated: true) }
                    return
                }
                if !answered {
                    answered = true
                    if GKLocalPlayer.local.isAuthenticated {
                        call.resolve(["authenticated": true, "name": GKLocalPlayer.local.displayName])
                    } else {
                        call.resolve(["authenticated": false, "error": error?.localizedDescription ?? ""])
                    }
                }
            }
        }
    }

    @objc func status(_ call: CAPPluginCall) {
        call.resolve(["authenticated": GKLocalPlayer.local.isAuthenticated])
    }

    @objc func submitScore(_ call: CAPPluginCall) {
        guard GKLocalPlayer.local.isAuthenticated else { call.reject("not_authenticated"); return }
        guard let leaderboardId = call.getString("leaderboardId"), let score = call.getInt("score") else {
            call.reject("leaderboardId and score are required"); return
        }
        GKLeaderboard.submitScore(score, context: 0, player: GKLocalPlayer.local, leaderboardIDs: [leaderboardId]) { error in
            if let error = error { call.reject(error.localizedDescription) } else { call.resolve() }
        }
    }

    @objc func reportAchievement(_ call: CAPPluginCall) {
        guard GKLocalPlayer.local.isAuthenticated else { call.reject("not_authenticated"); return }
        guard let achievementId = call.getString("achievementId") else { call.reject("achievementId is required"); return }
        let achievement = GKAchievement(identifier: achievementId)
        achievement.percentComplete = call.getDouble("percent") ?? 100.0
        achievement.showsCompletionBanner = true
        GKAchievement.report([achievement]) { error in
            if let error = error { call.reject(error.localizedDescription) } else { call.resolve() }
        }
    }

    @objc func showLeaderboard(_ call: CAPPluginCall) {
        guard GKLocalPlayer.local.isAuthenticated else { call.reject("not_authenticated"); return }
        let leaderboardId = call.getString("leaderboardId") ?? ""
        DispatchQueue.main.async { [weak self] in
            guard let self = self else { return }
            let gc = GKGameCenterViewController(leaderboardID: leaderboardId, playerScope: .global, timeScope: .allTime)
            gc.gameCenterDelegate = self
            self.bridge?.viewController?.present(gc, animated: true)
            call.resolve()
        }
    }

    @objc func showAchievements(_ call: CAPPluginCall) {
        guard GKLocalPlayer.local.isAuthenticated else { call.reject("not_authenticated"); return }
        DispatchQueue.main.async { [weak self] in
            guard let self = self else { return }
            let gc = GKGameCenterViewController(state: .achievements)
            gc.gameCenterDelegate = self
            self.bridge?.viewController?.present(gc, animated: true)
            call.resolve()
        }
    }

    public func gameCenterViewControllerDidFinish(_ gameCenterViewController: GKGameCenterViewController) {
        gameCenterViewController.dismiss(animated: true)
    }
}
