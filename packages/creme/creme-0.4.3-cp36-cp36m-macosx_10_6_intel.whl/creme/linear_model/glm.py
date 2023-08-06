import collections
import numbers

from .. import base
from .. import optim
from .. import utils


class GLM:
    """Generalized Linear Model.

    Parameters:
        optimizer (optim.Optimizer): The sequential optimizer used for updating the weights. Note
            that the intercept is handled separately.
        loss (optim.Loss): The loss function to optimize for.
        intercept (float): Initial intercept value.
        intercept_lr (optim.schedulers.Scheduler or float): Learning rate scheduler used for
            updating the intercept. If a `float` is passed, then an instance of
            `optim.schedulers.Constant` will be used. Setting this to 0 implies that the intercept
            will be not be updated. Setting this to 0 means that no intercept will be used.
        l2 (float): Amount of L2 regularization used to push weights towards 0.
        clip_gradient (float): Clips the absolute value of each gradient value.

    Attributes:
        weights (collections.defaultdict)

    """

    def __init__(self, optimizer, loss, l2, intercept, intercept_lr, clip_gradient):
        self.optimizer = optimizer
        self.loss = loss
        self.l2 = l2
        self.intercept = intercept
        self.intercept_lr = (
            optim.schedulers.Constant(intercept_lr)
            if isinstance(intercept_lr, numbers.Number) else
            intercept_lr
        )
        self.clip_gradient = clip_gradient
        self.weights = collections.defaultdict(float)

    def _raw_dot(self, x):
        return utils.math.dot(self.weights, x) + self.intercept

    def fit_one(self, x, y):

        # Some optimizers need to do something before a prediction is made
        self.weights = self.optimizer.update_before_pred(w=self.weights)

        # Obtain the gradient of the loss with respect to the raw output
        g_loss = self.loss.gradient(y_true=y, y_pred=self._raw_dot(x))

        # Calculate the gradient
        gradient = {
            i: utils.math.clamp(
                x=xi * g_loss + 2. * self.l2 * self.weights.get(i, 0),
                minimum=-self.clip_gradient,
                maximum=self.clip_gradient
            )
            for i, xi in x.items()
        }

        # Update the intercept
        self.intercept -= self.intercept_lr.get(self.optimizer.n_iterations) * g_loss

        # Update the weights
        self.weights = self.optimizer.update_after_pred(w=self.weights, g=gradient)

        return self


class LinearRegression(GLM, base.Regressor):
    """Linear regression.

    Parameters:
        optimizer (optim.Optimizer): The sequential optimizer used for updating the weights. Note
            that the intercept is handled separately. Defaults to ``optim.SGD(.01)``.
        loss (optim.RegressionLoss): The loss function to optimize for. Defaults to
            ``optim.SquaredLoss``.
        intercept (float): Initial intercept value.
        intercept_lr (optim.schedulers.Scheduler or float): Learning rate scheduler used for
            updating the intercept. If a `float` is passed, then an instance of
            `optim.schedulers.Constant` will be used. Setting this to 0 implies that the intercept
            will be not be updated.
        l2 (float): Amount of L2 regularization used to push weights towards 0.

    Attributes:
        weights (collections.defaultdict): The current weights assigned to the features.

    Example:

        ::

            >>> from creme import linear_model
            >>> from creme import metrics
            >>> from creme import model_selection
            >>> from creme import preprocessing
            >>> from creme import stream
            >>> from sklearn import datasets

            >>> X_y = stream.iter_sklearn_dataset(
            ...     dataset=datasets.load_boston(),
            ...     shuffle=True,
            ...     random_state=42
            ... )
            >>> model = (
            ...     preprocessing.StandardScaler() |
            ...     linear_model.LinearRegression(intercept_lr=.1)
            ... )
            >>> metric = metrics.MAE()

            >>> model_selection.online_score(X_y, model, metric)
            MAE: 4.038404

            >>> model['LinearRegression'].intercept
            22.189736...

    Note:
        Using a feature scaler such as `preprocessing.StandardScaler` upstream helps the optimizer
        to converge.

    """

    def __init__(self, optimizer=None, loss=None, l2=.0001, intercept=0., intercept_lr=.01,
                 clip_gradient=1e12):
        super().__init__(
            optimizer=(
                optim.SGD(optim.schedulers.InverseScaling(.01, .25))
                if optimizer is None else
                optimizer
            ),
            loss=optim.losses.Squared() if loss is None else loss,
            intercept=intercept,
            intercept_lr=intercept_lr,
            l2=l2,
            clip_gradient=clip_gradient
        )

    def predict_one(self, x):
        return self._raw_dot(x)


class LogisticRegression(GLM, base.BinaryClassifier):
    """Logistic regression.

    Parameters:
        optimizer (optim.Optimizer): The sequential optimizer used for updating the weights. Note
            that the intercept is handled separately. Defaults to ``optim.SGD(.05)``.
        loss (optim.BinaryLoss): The loss function to optimize for. Defaults to ``optim.LogLoss``.
        intercept (float): Initial intercept value.
        intercept_lr (optim.schedulers.Scheduler or float): Learning rate scheduler used for
            updating the intercept. If a `float` is passed, then an instance of
            `optim.schedulers.Constant` will be used. Setting this to 0 implies that the intercept
            will be not be updated.
        l2 (float): Amount of L2 regularization used to push weights towards .

    Attributes:
        weights (collections.defaultdict)

    Example:

        ::

            >>> from creme import datasets
            >>> from creme import linear_model
            >>> from creme import metrics
            >>> from creme import model_selection
            >>> from creme import optim
            >>> from creme import preprocessing

            >>> X_y = datasets.fetch_electricity()

            >>> model = (
            ...     preprocessing.StandardScaler() |
            ...     linear_model.LogisticRegression(optimizer=optim.SGD(.1))
            ... )
            >>> metric = metrics.Accuracy()

            >>> model_selection.online_score(X_y, model, metric)
            Accuracy: 0.894664

    Note:
        Using a feature scaler such as `preprocessing.StandardScaler` upstream helps the optimizer
        to converge.

    """

    def __init__(self, optimizer=None, loss=None, l2=.0001, intercept=0., intercept_lr=.01,
                 clip_gradient=1e12):
        super().__init__(
            optimizer=optim.SGD(.01) if optimizer is None else optimizer,
            loss=optim.losses.Log() if loss is None else loss,
            intercept=intercept,
            intercept_lr=intercept_lr,
            l2=l2,
            clip_gradient=clip_gradient
        )

    def predict_proba_one(self, x):
        p = utils.math.sigmoid(self._raw_dot(x))  # Convert log-odds ratio to probability
        return {True: p, False: 1. - p}
